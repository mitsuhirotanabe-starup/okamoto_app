import streamlit as st
from const import label_to_group, group_to_step2, group_to_step3, group_to_label
import json


def init_potential_node():
    # defect_nameがNoneの場合のガード処理
    if st.session_state.defect_name is None:
        st.session_state.potential_node = []
        return

    group_id = label_to_group.get(st.session_state.defect_name)
    if group_id is None:
        st.session_state.potential_node = []
        return

    label_list = group_to_label.get(group_id, [])
    st.session_state.potential_node = []
    
    for label in label_list:
       try:
           json_path = f"./json_data/{label}.json"
           with open(json_path, 'r', encoding='utf-8') as f:
               json_data = json.load(f)
               for node in json_data.get("terminals", []):
                   st.session_state.potential_node.append(node)
       except FileNotFoundError:
           st.warning(f"データファイルが見つかりません: {json_path}")
       except json.JSONDecodeError:
           st.error(f"JSONファイルの読み込みに失敗しました: {json_path}")
 
def detect_terminals():
    # potential_nodeが存在しない、またはNoneの場合は初期化
    if 'potential_node' not in st.session_state or st.session_state.potential_node is None:
        init_potential_node()
    
    # それでもNoneなら空リストにする（安全策）
    if st.session_state.potential_node is None:
        st.session_state.potential_node = []
    
    confirmed_koumoku = st.session_state.get('kakunin_koumoku', {})
    confirmed_koutei = st.session_state.get('koutei_kakunin', {})
    q_and_a = {**confirmed_koumoku, **confirmed_koutei}
    
    remaining_nodes = []
    
    for node in st.session_state.potential_node:
        match = True
        t1 = node.get("t1", [])
        
        # 質問と回答の照合ロジック
        # ここでは「回答済みの質問」についてのみチェックを行う
        # ユーザーの回答(a)と、ノードの条件(condition["a"])が一致しない場合のみ除外        
        for condition in t1:
            q_code = condition["q"]
            expected_a = condition["a"]
            
            # ユーザーがこの質問に回答しているか確認
            if q_code in q_and_a:
                user_a = q_and_a[q_code]
                
                # ユーザーの回答が「不明」なら判定材料にしない（スキップ）
                if user_a == "不明":
                    continue
                
                # 回答が食い違っていたらマッチしない
                if user_a != expected_a:
                    match = False
                    break
        
        if match:
            remaining_nodes.append(node)
            
    # フィルタリング後のリストで更新
    st.session_state.potential_node = remaining_nodes
    
    return remaining_nodes

def load_questions():
    json_path = "./json_data/questions.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)["questions"]
        st.session_state.questions_data = questions_data
    return questions_data



def show_results():
    st.write("ステップ4：診断結果表示")
    st.write("ここに診断結果を表示します。")
    
    # 診断実行
    detect_terminals()
    
    if not st.session_state.potential_node:
        st.warning("条件に一致する候補が見つかりませんでした。")
    else:
        for i, node in enumerate(st.session_state.potential_node):
            with st.container(border=True):
                st.write(f"### [結果候補 {i+1}]", f"ID: {node['id']}")
                st.write(node.get('label', 'N/A'))                
            if i >= 4:
                break
    
    st.button("最初に戻る", on_click=lambda: st.session_state.update(step=1, step1_option=0, defect_name=None, kakunin_koumoku={}, koutei_kakunin={}, potential_node=None), type="primary")

def show_questions():
    load_questions()
    
    st.write("追加質問")
    remaining_questions_code = []
    for node in st.session_state.potential_node:
        t2 = node.get("t2", [])
        r = node.get("r", [])
        remaining = t2 + r
        for condition in remaining:
            q_code = condition["q"]
            if (q_code not in remaining_questions_code) and (q_code not in st.session_state.kakunin_koumoku) and (q_code not in st.session_state.koutei_kakunin):
                remaining_questions_code.append(q_code)
                
    if not remaining_questions_code:
        st.info("追加の質問はありません。")
        return
    
    st.write("以下の質問に回答してください：")
    remaining_questions = [q for q in st.session_state.questions_data if q["code"] in remaining_questions_code]
    for q in remaining_questions:
        # 質問の要件がある場合、チェックして表示/非表示を制御
        is_show = True
        if "requirements" in q:
            for dict in q["requirements"]:
                if st.session_state.koutei_kakunin.get(dict["q"], None) != dict["a"]:
                    is_show = False
                    break
            
        if is_show:
            options = q.get("option", ["不明"]) if "option" in q else ["Yes", "No", "不明"]
            # デフォルトのインデックスを安全に設定
            # "不明"が含まれていればそれを選択、なければ最後の要素を選択、それもなければ0
            default_index = 0
            if "不明" in options:
                default_index = options.index("不明")
            elif len(options) > 0:
                default_index = len(options) - 1
                
            st.radio(
                q["label"], 
                options,
                index=default_index, 
                on_change=lambda code=q["code"]: st.session_state.koutei_kakunin.update({code: st.session_state.koutei_kakunin[code]})
            )
        
     