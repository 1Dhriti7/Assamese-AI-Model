import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="অসমীয়া AI", page_icon="🗣️")
st.title("🗣️ অসমীয়া AI চেটবট")
st.caption("মই অসমীয়াত কথা পাতোঁ। যিকোনো প্ৰশ্ন কৰক।")

# API Key input
api_key = st.text_input("Gemini API Key দিয়ক", type="password")
if api_key:
    genai.configure(api_key=api_key)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("ইয়াত লিখক..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if api_key:
        with st.chat_message("assistant"):
            model = genai.GenerativeModel('gemini-3.6-flash')
            full_prompt = f"You are a helpful assistant. Reply ONLY in Assamese language and Assamese script. User question: {prompt}"
            response = model.generate_content(full_prompt)
            reply = response.text
            st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
    else:
        st.warning("প্ৰথমে API Key দিয়ক")