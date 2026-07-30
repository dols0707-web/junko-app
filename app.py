import streamlit as st
from google import genai
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
    # 최신 SDK 클라이언트 생성
    client = genai.Client(api_key=api_key)

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
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config={
                    'system_instruction': '너는 친근하고 다정한 한국어 AI 친구 준코야. 항상 반말조로 친절하고 자연스러운 한국어로 대답해줘.'
                }
            )
            reply = response.text

            # 준코 답변 표시 및 저장
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            # 사용량 제한(429/Quota) 에러 시 친절한 한국어 안내
            if "429" in str(e) or "quota" in str(e).lower():
                st.warning("⏳ 말을 너무 빨리 걸었나 봐! 20~30초만 기다렸다가 다시 말해줘~")
            else:
                st.error(f"오류가 발생했습니다: {e}")
