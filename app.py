            response = model.generate_content(prompt)
            reply = response.text

            # 준코 답변 표시 및 저장
            with st.chat_message("assistant"):
                st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
