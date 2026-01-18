import streamlit as st
import json
from datetime import datetime
from PIL import Image, ImageFilter
from model.model import predict
from streamlit_cropper import st_cropper
from page.input_selection_page import input_selection
from page.question_page import question_page
from page.show_results_page import show_results, show_questions
from style import custom_css
import time
import textwrap

st.set_page_config(
    page_title="不良診断アシスタント(Streamlit)",
    page_icon="🧠",
    layout="wide" # "wide" よりも "centered" の方が元のUIに近い
)

# カスタムCSSの注入 (Tailwindの雰囲気を再現)
st.markdown(custom_css, unsafe_allow_html=True)

# セッションステートの初期化

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'step1_option' not in st.session_state:
    st.session_state.step1_option = 0
if 'is_uploaded' not in st.session_state:
    st.session_state.is_uploaded = False
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'prediction_results' not in st.session_state:
    st.session_state.prediction_results = None
if 'defect_name' not in st.session_state:
    st.session_state.defect_name = None
if 'answer' not in st.session_state:
    st.session_state.answer = {}
if 'save_step' not in st.session_state:
    st.session_state.save_step = 1

# 状態の取得
current_step = st.session_state.step
total_steps = 4
progress_val = int((current_step / total_steps) * 100)
step_names = {1: "不良名選択", 2: "状況確認", 3: "工程確認", 4: "診断結果"}
current_time = time.strftime('%H:%M:%S')

# HTML 文字列の構築 (f-string を使用)
header_and_progress_html = textwrap.dedent(f"""\
<div class="brand-header" style="
    position: fixed; top: 0; left: 0; width: 100%; 
    background-color: #008080; color: white; padding: 15px 30px; 
    z-index: 1000; display: flex; justify-content: space-between; align-items: center;
">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-style: italic; font-weight: bold;">鋳造不良判定アシスタント</span>
    </div>
    <div style="font-size: 0.8rem; opacity: 0.8;">{current_time}</div>
</div>

<div class="progress-wrapper" style="
    position: fixed; top: 60px; left: 0; width: 100%; 
    background-color: white; padding: 15px 50px; z-index: 999; 
    border-bottom: 1px solid #e2e8f0;
">
    <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
        <span style="font-weight: bold; color: #64748b; font-size: 0.9rem;">
            ステップ {current_step} / {total_steps} : 
            <span style="color: #008080;">{step_names[current_step]}</span>
        </span>
        <span style="font-weight: 900; color: #334155; font-size: 1.1rem;">{progress_val}%</span>
    </div>
    <div style="width: 100%; background-color: #f1f5f9; border-radius: 10px; height: 8px; overflow: hidden;">
        <div style="width: {progress_val}%; background-color: #008080; height: 100%; transition: width 0.5s ease-in-out;"></div>
    </div>
</div>
""").strip()

st.markdown(header_and_progress_html, unsafe_allow_html=True)
st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)



if st.session_state.step == 1:
    input_selection(st.session_state.step1_option)
    
elif st.session_state.step == 2:
    question_page(step=2)
    
elif st.session_state.step == 3:
    question_page(step=3)
    
elif st.session_state.step == 4:
    show_results()