import streamlit as st
import json
from datetime import datetime
from PIL import Image, ImageFilter
from model.model import predict
from streamlit_cropper import st_cropper
from const import label_name, ja_to_en_label, en_to_ja_label

def handle_uploading_image(key):
    if st.session_state[key] is not None:
        st.session_state.uploaded_image = st.session_state[key]
        st.session_state.is_uploaded = True
    

def input_selection(step1_option):
    if step1_option == 0: 
        with st.container(border=True):
            st.write("### 📷カメラ撮影")
            col1, col2 = st.columns([4,1])
            with col1:
                st.write("カメラで不良箇所を撮影して不良判定を行います。")
            with col2:
                st.button("カメラ起動", use_container_width=True, on_click=lambda: st.session_state.update(step1_option=1), type="primary")         
        with st.container(border=True):
            st.write("### 🖼️画像アップロード")
            col1, col2 = st.columns([4,1])
            with col1:
                st.write("既存の不良鋳造画像をアップロードして不良判定を行います。")
            with col2:
                st.button("画像選択", use_container_width=True, on_click=lambda: st.session_state.update(step1_option=2), type="primary")
            
        with st.container(border=True):
            st.write("### 📜不良名を選択")
            col1, col2 = st.columns([4,1])
            with col1:
                st.write("不良名を選択して不良診断を行います。")
            with col2:
                st.button("不良名選択", use_container_width=True, on_click=lambda: st.session_state.update(step1_option=3), type="primary")
        with st.container(border=True):
            st.write("### 💾保存した途中から再開")
            col1, col2 = st.columns([4,1])
            with col1:
                st.write("保存した途中データから不良診断を再開します。")
            with col2:
                st.button("途中から再開", use_container_width=True, on_click=lambda: st.session_state.update(step=st.session_state.save_step), type="primary")
        
    elif step1_option == 1:
        if not st.session_state.is_uploaded:
            st.camera_input("カメラで不良箇所を撮影してください", key="camera_input", on_change=handle_uploading_image, args=('camera_input',))
            st.button("戻る", on_click=st.session_state.clear, args=())
            
        else:
            col1, col2 = st.columns([3,2])
            with col1:
                image = Image.open(st.session_state.uploaded_image)
                st.subheader("Uploaded Image")
                
                cropped_img = st_cropper(
                    img_file=image,
                    realtime_update=True,
                    box_color="#0000FF",
                    aspect_ratio=(1, 1),
                    return_type="image",
                )
                
                sub_col1, sub_col2, sub_col3 = st.columns([1,1,1])
                
                with sub_col1:
                    st.button("戻る", on_click=st.session_state.clear, args=(), use_container_width=True)
                with sub_col2:
                    st.button("再撮影", on_click=lambda: st.session_state.update(is_uploaded=False, uploaded_image=None), use_container_width=True)
                with sub_col3:
                    # 1. ボタンが押されたら結果をsession_stateに保存する
                    if st.button("不良判定を実行", use_container_width=True, type="primary"):
                        with st.spinner("不良判定中...しばらくお待ちください。"):
                            # 結果をsession_stateに保存
                            st.session_state.prediction_results = predict(cropped_img)
            
            with col2:
                # 2. 結果がsession_stateにあれば表示する（ボタンのブロックの外に出す）
                if st.session_state.prediction_results is not None:
                    results = st.session_state.prediction_results
                    
                    st.subheader("results")
                    
                    # 遷移用の関数を定義
                    def go_to_step2_with_defect(defect_name):
                        st.session_state.defect_name = defect_name
                        st.session_state.step = 2

                    for result in results:
                        with st.container(border=True):
                            col1, col2 = st.columns([4,1])
                            with col1:
                                st.write(f"**不良名：{en_to_ja_label[result['class_name']]}**")
                                st.write(f"確率：{result['probability']:.4f}")
                            with col2:
                                # 3. on_clickを使って確実に遷移させる
                                st.button(
                                    "進む", 
                                    key=f"select_{result['class_id']}",
                                    on_click=go_to_step2_with_defect,
                                    args=(result['class_name'],),
                                    type="primary",
                                    use_container_width=True
                                )
            
        
        
    elif step1_option == 2:
        if not st.session_state.is_uploaded:
            st.file_uploader("不良鋳造画像をアップロードしてください", type=["jpg", "jpeg", "png"], key="file_uploader", on_change=handle_uploading_image, args=('file_uploader',))
        else:
            col1, col2 = st.columns([3,2])
            with col1:
                image = Image.open(st.session_state.uploaded_image)
                st.subheader("Uploaded Image")
                
                cropped_img = st_cropper(
                    img_file=image,
                    realtime_update=True,
                    box_color="#0000FF",
                    aspect_ratio=(1, 1),
                    return_type="image",
                )
                
                sub_col1, sub_col2, sub_col3 = st.columns([1,1,1])
                
                with sub_col1:
                    st.button("戻る", on_click=st.session_state.clear, args=(), use_container_width=True)
                with sub_col2:
                    st.button("再アップロード", on_click=lambda: st.session_state.update(is_uploaded=False, uploaded_image=None), use_container_width=True)
                with sub_col3:
                    # 1. ボタンが押されたら結果をsession_stateに保存する
                    if st.button("不良判定を実行", use_container_width=True, type="primary"):
                        with st.spinner("不良判定中...しばらくお待ちください。"):
                            # 結果をsession_stateに保存
                            st.session_state.prediction_results = predict(cropped_img)
            
            with col2:
                # 2. 結果がsession_stateにあれば表示する（ボタンのブロックの外に出す）
                if st.session_state.prediction_results is not None:
                    results = st.session_state.prediction_results
                    
                    st.subheader("results")
                    
                    # 遷移用の関数を定義
                    def go_to_step2_with_defect(defect_name):
                        st.session_state.defect_name = defect_name
                        st.session_state.step = 2

                    for result in results:
                        with st.container(border=True):
                            col1, col2 = st.columns([4,1])
                            with col1:
                                st.write(f"**不良名：{en_to_ja_label[result['class_name']]}**")
                                st.write(f"確率：{result['probability']:.4f}")
                            with col2:
                                st.button(
                                    "進む", 
                                    key=f"select_{result['class_id']}",
                                    on_click=go_to_step2_with_defect,
                                    args=(result['class_name'],),
                                    type="primary",
                                    use_container_width=True
                                )
            
        st.button("戻る", on_click=st.session_state.clear, args=())
                    
    elif step1_option == 3:
        def go_to_step2():
            # ラジオボタンで選択された値を、永続的なsession_state変数にコピーする
            st.session_state.defect_name = ja_to_en_label[st.session_state.defect_name_selector]
            st.session_state.step = 2


        # ラジオボタンの呼び出し
        selected = st.radio(
            "不良名を選択してください",
            tuple(ja_to_en_label.keys()),
            horizontal=True,
            key="defect_name_selector"
        )
 
        col1, col2, col3 = st.columns([1,5,1])
        with col1:
            st.button("戻る", on_click=lambda: st.session_state.update(step=1, step1_option=0),use_container_width=True)
        with col3:
            st.button("次へ進む", on_click=go_to_step2, use_container_width=True, type="primary")
            
    else:
        st.write("不正なオプションです。")