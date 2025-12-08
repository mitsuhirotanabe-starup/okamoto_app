import streamlit as st
import json
from const import label_to_group, group_to_step2, group_to_step3

# 不良グループに基づいて質問をロード
@st.cache_data
def load_questions(defect_name, step):
    if not defect_name:
        return []
    group_id = label_to_group.get(defect_name, None)
    json_path = "./json_data/questions.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        questions_data = json.load(f)["questions"]
        if step == 2:
            questions_data = [q for q in questions_data if q["code"] in group_to_step2[str(group_id)]]
        else:
            questions_data = [q for q in questions_data if q["code"] in group_to_step3[str(group_id)]]
    for q in questions_data:
        st.session_state.answer[q["code"]] = "不明"
    return questions_data

# ただしくセッションに保存されるように更新関数を定義
def update_questions(question_code, step):
    # if step == 2:
    #     st.session_state.kakunin_koumoku[question_code] = st.session_state[question_code]
    # else:
    #     st.session_state.koutei_kakunin[question_code] = st.session_state[question_code]
    st.session_state.answer[question_code] = st.session_state[question_code]

# step 2: 確認項目
def kakunin_koumoku():
    st.write("確認項目")
    questions_data = load_questions(st.session_state.defect_name, step=2)
     
    if not questions_data:
        st.warning('質問が読み込めませんでした。')
        st.button("最初に戻る", on_click=lambda: st.session_state.update(step=1, step1_option=0, defect_name=None, answer={}), type="primary")
        return
    
    # if 'kakunin_koumoku' not in st.session_state:
    #     st.session_state.kakunin_koumoku = {}
        
    for q in questions_data:
        options = q.get("option") if "option" in q else ["Yes", "No", "不明"]
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
            key=q["code"], 
            on_change=update_questions, 
            args=(q["code"], 2)
        )
        
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: st.session_state.update(step=1))
    with col2:
        st.button("次へ進む", on_click=lambda: st.session_state.update(step=3), type="primary")
 
# step 3: 工程確認       
def koutei_kakunin():
    st.write("ステップ3：工程確認回答")
    questions_data = load_questions(st.session_state.defect_name, step=3)
    
    if not questions_data:
        st.warning('質問が読み込めませんでした。')
        st.button("最初に戻る", on_click=lambda: st.session_state.update(step=1, step1_option=0, defect_name=None, answer={}), type="primary")
        return
    
    # if 'koutei_kakunin' not in st.session_state:
    #     st.session_state.koutei_kakunin = {}
        
    for q in questions_data:
        # 質問の要件がある場合、チェックして表示/非表示を制御
        is_show = True
        if "requirements" in q:
            for dict in q["requirements"]:
                if st.session_state.answer.get(dict["q"], None) != dict["a"]:
                    is_show = False
                    break
            
        options = q.get("option") if "option" in q else ["Yes", "No", "不明"]
        # デフォルトのインデックスを安全に設定
        # "不明"が含まれていればそれを選択、なければ最後の要素を選択、それもなければ0
        default_index = 0
        if "不明" in options:
            default_index = options.index("不明")
        elif len(options) > 0:
            default_index = len(options) - 1
            
        if is_show:
            st.radio(
                q["label"], 
                options,
                index=default_index,
                key=q["code"], 
                on_change=update_questions, 
                args=(q["code"], 3)
            )
        
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("戻る", on_click=lambda: st.session_state.update(step=2))
    with col2:
        st.button("次へ進む", on_click=lambda: st.session_state.update(step=4), type="primary")