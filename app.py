import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 페이지 기본 설정
st.set_page_config(page_title="준코 친구", page_icon="🤖")
st.title("🤖 준코 친구")
st.write("안녕! 나는 너의 AI 친구 준코야. 무엇이든 편하게 물어봐!")

# API 키 설정 (Streamlit Secrets에서 불러옴)
api_key = st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning("Google Gemini API 키가 설정되지 않았습니다. Streamlit Secrets에 GEMINI_API_KEY를 추가해 주세요.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 대화 기록 세션 초기화
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
        with st.chat_message("assistant"):
            with st.spinner("준코가 생각 중..."):
                response = model.generate_content(prompt)
                reply_text = response.text
                st.markdown(reply_text)

                # gTTS를 이용한 음성 변환 (한국어)
                try:
                    tts = gTTS(text=reply_text, lang='ko')
                    audio_file = "response.mp3"
                    tts.save(audio_file)
                    st.audio(audio_file, format="audio/mp3")
                except Exception as e:
                    st.error(f"음성 생성 중 오류 발생: {e}")

        # 답변 저장
        st.session_state.messages.append({"role": "assistant", "content": reply_text})
