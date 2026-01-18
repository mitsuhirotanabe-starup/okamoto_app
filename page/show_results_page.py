import streamlit as st
from const import label_to_group, group_to_step2, group_to_step3, group_to_label
import json

def update_questions(code, key):
    st.session_state.answer[code] = st.session_state[key]
              
                
def init_potential_node():
    group_id = label_to_group.get(st.session_state.defect_name)
    label_list = group_to_label.get(group_id, [])
    st.session_state.potential_node = []
    
    for label in label_list:
       try:
           json_path = f"./json_data/terminals/{label}.json"
           with open(json_path, 'r', encoding='utf-8') as f:
               json_data = json.load(f)
               for node in json_data.get("terminals", []):
                   st.session_state.potential_node.append(node)
       except FileNotFoundError:
           st.warning(f"データファイルが見つかりません: {json_path}")
       except json.JSONDecodeError:
           st.error(f"JSONファイルの読み込みに失敗しました: {json_path}")
           
           
def load_cause_and_solution():
    json_path = "./json_data/cause_and_solution.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        cause_and_solution_data = json.load(f)
        st.session_state.cause_and_solution_data = cause_and_solution_data
    


 
def detect_terminals():
    # step4に来たときに一度だけ初期化
    if 'potential_node' not in st.session_state or st.session_state.potential_node is None:
        init_potential_node()
    if 'potential_cause_and_solution' not in st.session_state or st.session_state.potential_cause_and_solution is None:
        load_cause_and_solution()
    
    # それでもNoneなら空リストにする（安全策）
    if st.session_state.potential_node is None:
        st.session_state.potential_node = []
    
    remaining_nodes = []
    remaining_cause_and_solution = []
    
    for node in st.session_state.potential_node:
        match = True
        q_len = 0
        correct = 0
        q_list = ["t1", "t2", "r"]
        
        for q_key in q_list:
            q = node.get(q_key, [])
            if q_key != "r":
                # t1, t2の数
                q_len += len(q)
                
            # 質問と回答の照合ロジック
            # ここでは「回答済みの質問」についてのみチェックを行う
            # ユーザーの回答(a)と、ノードの条件(condition["a"])が一致しない場合のみ除外        
            for condition in q:
                q_code = condition["q"]
                expected_a = condition["a"]
                is_list = isinstance(expected_a, list)
                
                # ユーザーがこの質問に回答しているか確認
                if q_code in st.session_state.answer:
                    user_a = st.session_state.answer[q_code]
                    
                    # ユーザーの回答が「不明」なら判定材料にしない（スキップ）
                    if user_a == "不明":
                        continue
                    
                    # 回答が食い違っていたらマッチしない
                    # expected_aがリストかどうかで場合分け
                    if is_list and user_a not in expected_a:
                        match = False
                        break
                    elif not is_list and user_a != expected_a:
                        match = False
                        break
                    elif q_key != "r":
                        # t1, t2で一致した場合のみ正解数をカウント
                        correct += 1
            
            if match:
                node["score_a"] = correct
                node["score_b"] = q_len - correct
                remaining_nodes.append(node)

    # IDに基づいて重複を排除する
    # 辞書を使ってIDをキーにすることで重複を取り除き、リストに戻します
    unique_nodes_dict = {node['id']: node for node in remaining_nodes}
    remaining_nodes = list(unique_nodes_dict.values())

    # フィルタリング後のリストで更新
    remaining_nodes = sorted(remaining_nodes, key=lambda x: (x.get("score_a", 0), -x.get("score_b", 0)), reverse=True)
    st.session_state.potential_node = remaining_nodes
    
    # もし先頭が"is_below == True"なら順位を下げる
    can_top_idx = next((idx for idx, node in enumerate(st.session_state.potential_node) if not node.get("is_below", False)), None)
    if can_top_idx is not None and can_top_idx > 0:
        st.session_state.potential_node[0], st.session_state.potential_node[can_top_idx] = st.session_state.potential_node[can_top_idx], st.session_state.potential_node[0]
    
    # 残った終端ノードを、原因と対策データに変換
    for i, node in enumerate(remaining_nodes):
        for cs in st.session_state.cause_and_solution_data:
            if node["id"] in cs["belong"]:
                remaining_cause_and_solution.append(cs)
                break
    
    # 重複を排除して返す（辞書はハッシュ不可なので、IDを使って重複判定を行う）
    unique_cs_dict = {}
    for cs in remaining_cause_and_solution:
        # cs["id"] をキーにして重複を防ぐ（古い値を上書きしない、あるいは上書きする）
        # 順番を保持したい＆最初のものを優先したいなら、まだキーがない時だけ追加する
        if cs["id"] not in unique_cs_dict:
            unique_cs_dict[cs["id"]] = cs
            
    remaining_cause_and_solution = list(unique_cs_dict.values())
    st.session_state.potential_cause_and_solution = remaining_cause_and_solution

def load_questions():
    json_path = "./json_data/questions.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)["questions"]
        st.session_state.questions_data = questions_data
    return questions_data


def show_questions(cs):
    if 'questions_data' not in st.session_state or st.session_state.questions_data is None:
        load_questions()
    
    nodes = cs.get("belong", {})
    node = next((n for n in st.session_state.potential_node if n["id"] in nodes), None)
    remaining_questions_code = []
    t1 = node.get("t1", [])
    t2 = node.get("t2", [])
    r = node.get("r", [])
    remaining = t1 + t2 + r
    for condition in remaining:
        q_code = condition["q"]
        if q_code not in st.session_state.answer:
            remaining_questions_code.append(q_code)
                
    if not remaining_questions_code:
        st.info("追加の質問はありません。")
        return
    
    remaining_questions = [q for q in st.session_state.questions_data if q["code"] in remaining_questions_code]
    
    with st.expander("追加質問"):
        for q in remaining_questions:
            # 質問の要件がある場合、チェックして表示/非表示を制御
            is_show = True
            if "requirements" in q:
                for dict in q["requirements"]:
                    if st.session_state.answer.get(dict["q"], None) != dict["a"]:
                        is_show = False
                        break
                
            if is_show:
                options = q.get("option") if "option" in q else ["Yes", "No", "不明"]

                default_index = 0
                if "不明" in options:
                    default_index = options.index("不明")
                elif len(options) > 0:
                    default_index = len(options) - 1

                # 「ノードID+質問コード」にして一意化
                node_id = str(node.get("id", "unknown"))
                widget_key = f"radio_{node_id}_{q['code']}"
                    
                with st.container(border=True):
                    st.radio(
                        q["label"], 
                        options,
                        index=default_index, 
                        key=widget_key,
                        on_change=update_questions, 
                        args=(q["code"], widget_key),
                        horizontal=True,
                    )
                    
def show_results():
    # 診断実行
    detect_terminals()
    
    if not st.session_state.potential_cause_and_solution:
        st.warning("条件に一致する候補が見つかりませんでした。")
    else:
        for i, cs in enumerate(st.session_state.potential_cause_and_solution):
            with st.container(border=True):
                # causeが空文字でなければ表示
                if cs["cause"].strip():
                    st.markdown(f""" **原因：{cs["cause"]}**""")
                # solutionが空文字でなければ表示
                if cs["solution"].strip():
                    st.markdown(f""" **対策：{cs["solution"]}**""")
                show_questions(cs)             
            if i >= 4:
                break
    col1, col2, col3, col4 = st.columns([1,1,1,5])
    with col1:
        st.button("最初に戻る", on_click=lambda: st.session_state.update(step=1, step1_option=0, defect_name=None, answer={}, potential_node=None), use_container_width=True)
    with col2:
        st.button("一旦保存して終了", on_click=lambda: st.session_state.update(step=1, save_step=4, step1_option=0), use_container_width=True)
    with col3:
        st.button("戻る", on_click=lambda: st.session_state.update(step=3), use_container_width=True)
                
