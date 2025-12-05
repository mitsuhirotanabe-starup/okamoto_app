import streamlit as st
import json
from datetime import datetime
from PIL import Image, ImageFilter
from model.model import predict
from streamlit_cropper import st_cropper

def input_selection(step1_option):
    if step1_option == 0:
        st.write("ステップ1：入力方法を選択")
        # with st.container(border=True):
        #     col1, col2 = st.columns([4,1])
        #     with col1:
        #         st.write("### 不良撮影")
        #         st.write("カメラを起動して不良箇所の撮影を行います。")
        #     with col2:
        #         st.button("カメラ起動", on_click=lambda: st.session_state.update(step1_option=1), type="primary")
            
        with st.container(border=True):
            col1, col2 = st.columns([4,1])
            with col1:
                st.write("### 画像アップロード")
                st.write("既存の不良鋳造画像をアップロードして不良判定を行います。")
            with col2:
                st.button("画像選択", on_click=lambda: st.session_state.update(step1_option=2), type="primary")
            
        with st.container(border=True):
            col1, col2 = st.columns([4,1])
            with col1:
                st.write("### 不良名を選択")
                st.write("不良名を選択して不良診断を行います。")
            with col2:
                st.button("不良名選択", on_click=lambda: st.session_state.update(step1_option=3), type="primary")

    elif step1_option == 1:
        st.write("不良撮影")
        st.button("カメラ起動（仮）")
        st.button("戻る", on_click=lambda: st.session_state.update(step1_option=0))
        
    elif step1_option == 2:
        uploaded_image = st.file_uploader("不良鋳造画像をアップロードしてください", type=["jpg", "jpeg", "png"], key="file_uploader")

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.subheader("Uploaded Image:")
            
            cropped_img = st_cropper(
                img_file=image,
                realtime_update=True,
                box_color="#0000FF",
                aspect_ratio=(1, 1),
                return_type="image",
            )
            
            # 1. ボタンが押されたら結果をsession_stateに保存する
            if st.button("不良判定を実行"):
                with st.spinner("不良判定中...しばらくお待ちください。"):
                    # 結果をsession_stateに保存
                    st.session_state.prediction_results = predict(cropped_img)
            
            # 2. 結果がsession_stateにあれば表示する（ボタンのブロックの外に出す）
            if st.session_state.prediction_results is not None:
                results = st.session_state.prediction_results
                
                st.subheader("不良判定結果:")
                
                # 遷移用の関数を定義
                def go_to_step2_with_defect(defect_name):
                    st.session_state.defect_name = defect_name
                    st.session_state.step = 2

                for result in results:
                    with st.container(border=True):
                        col1, col2 = st.columns([4,1])
                        with col1:
                            st.write(f"### 不良名：{result['class_name']}")
                            st.write(f"確率：{result['probability']:.4f}")
                        with col2:
                            # 3. on_clickを使って確実に遷移させる
                            st.button(
                                "進む", 
                                key=f"select_{result['class_id']}",
                                on_click=go_to_step2_with_defect,
                                args=(result['class_name'],)
                            )
            
        st.button("戻る", on_click=lambda: st.session_state.update(step1_option=0))
                    
    elif step1_option == 3:
        def go_to_step2():
            # ラジオボタンで選択された値を、永続的なsession_state変数にコピーする
            st.session_state.defect_name = st.session_state.defect_name_selector
            st.session_state.step = 2
            
        st.write("不良名を選択")
        st.radio("不良名を選択してください", ("sunakui", "kirai", "dakon", "arasare", "yumawari"), key="defect_name_selector")
        col1, col2 = st.columns([4,1])
        with col1:
            st.button("戻る", on_click=lambda: st.session_state.update(step1_option=0))
        with col2:
            st.button("次へ", on_click=go_to_step2, type="primary")
        
        
    else:
        st.write("不正なオプションです。")