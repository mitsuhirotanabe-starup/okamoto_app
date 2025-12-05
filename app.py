import streamlit as st
import json
from datetime import datetime
from PIL import Image, ImageFilter
from model.model import predict
from streamlit_cropper import st_cropper
from page.input_selection_page import input_selection
from page.question_page import kakunin_koumoku, koutei_kakunin
from page.show_results_page import show_results, show_questions

costom_css = """
<style>
.stButton>button {
    width: 100%;
}
</style>
"""

st.set_page_config(
    page_title="不良診断アシスタント(Streamlit)",
    page_icon="🧠",
    layout="centered" # "wide" よりも "centered" の方が元のUIに近い
)

if 'step' not in st.session_state:
    st.session_state.step = 1
if 'step1_option' not in st.session_state:
    st.session_state.step1_option = 0
if 'prediction_results' not in st.session_state:
    st.session_state.prediction_results = None
if 'defect_name' not in st.session_state:
    st.session_state.defect_name = None
if 'kakunin_koumoku' not in st.session_state:
    st.session_state.kakunin_koumoku = {}
if 'koutei_kakunin' not in st.session_state:
    st.session_state.koutei_kakunin = {}
if 'potential_node' not in st.session_state:
    st.session_state.potential_node = None
if 'questions_data' not in st.session_state:
    st.session_state.questions_data = None


st.title("不良診断アシスタント (Streamlit)")

if st.session_state.step == 1:
    input_selection(st.session_state.step1_option)
    
elif st.session_state.step == 2:
    kakunin_koumoku()
    
elif st.session_state.step == 3:
    koutei_kakunin()
    
elif st.session_state.step == 4:
    show_results()
    show_questions()