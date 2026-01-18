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

# 回答を更新する関数
def update_questions(question_code, step):
    st.session_state.answer[question_code] = st.session_state[question_code]


def question_page(step=2):    
    questions_data = load_questions(st.session_state.defect_name, step=step)
    if not questions_data:
        st.warning('質問が読み込めませんでした。')
        st.button("最初に戻る", on_click=lambda: st.session_state.update(step=1, step1_option=0, defect_name=None, answer={}), type="primary")
        return

    for q in questions_data:
        
        is_show = True
        if "requirements" in q:
            for requirements_dict in q["requirements"]:
                if st.session_state.answer.get(requirements_dict["q"], None) != requirements_dict["a"]:
                    is_show = False
                    break
            
        options = q.get("option") if "option" in q else ["Yes", "No", "不明"]
        default_index = 0
        if "不明" in options:
            default_index = options.index("不明")
        elif len(options) > 0:
            default_index = len(options) - 1
        
        # 一旦保存している回答をセット
        if q["code"] in st.session_state.answer:
            default_index = options.index(st.session_state.answer[q["code"]])
            
        # カードのすぐ下に（あるいは重なるように）ラジオボタンを配置
        # label_visibility="collapsed" でデフォルトのラベルを消す
        if is_show:
            # カードの開始
            with st.container(border=True):
                st.radio(
                    q["label"], 
                    options,
                    index=default_index,
                    key=q["code"], 
                    on_change=update_questions, 
                    args=(q["code"], 3),
                    horizontal=True,
                )
            
    col1, col2, col3, col4, col5 = st.columns([1,1,1,4,1])
    with col1:
        st.button("最初に戻る", on_click=st.session_state.clear, args=(), use_container_width=True)
    with col2:
        st.button("一旦保存", on_click=lambda: st.session_state.update(step=1, save_step=step, step1_option=0), use_container_width=True)
    with col3:
        st.button("戻る", on_click=lambda: st.session_state.update(step=step-1), use_container_width=True)
    with col5:
        st.button("次へ進む", on_click=lambda: st.session_state.update(step=step+1), type="primary", use_container_width=True)
            