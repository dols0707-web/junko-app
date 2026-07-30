import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 페이지 기본 설정
st.set_page_config(page_title="준코 친구", page_icon="🤖")
st.title("🤖 준코 친구")
st.write("안녕! 나는 너의 AI 친구 준코야. 무엇이든 편하게 물어봐!")

# API 키 설정
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("Google Gemini API 키가 설정되지 않았습니다.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    # 대화 기록 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 이전 대화 내용 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력 처리
    if prompt := st.chat_input("준코에게 말을 걸어보세요..."):
        # 사용자 메시지 표시 및 저장
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Gemini 답변 생성
        try:
            response = model.generate_content(prompt)
            reply = response.text

            # 준코 답변 표시 및 저장
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
