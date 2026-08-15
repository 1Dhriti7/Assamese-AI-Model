import streamlit as st
import google.generativeai as genai
import os
import datetime
import pytz

# Page config
st.set_page_config(page_title="অসমীয়া AI চেটবট", page_icon="🗣️", layout="centered")

st.title("🗣️ অসমীয়া AI চেটবট")
st.write("মই অসমীয়াত কথা পাতোঁ। যিকোনো প্ৰশ্ন কৰক।")

# Get API Key from Secrets first, else ask user
if "GOOGLE_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
else:
    GOOGLE_API_KEY = st.text_input("Gemini API Key দিয়ক", type="password")

if not GOOGLE_API_KEY:
    st.warning("অনুগ্ৰহ কৰি API Key দিয়ক")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# Get current date and time for Assam
tz = pytz.timezone("Asia/Kolkata")
now = datetime.datetime.now(tz)
current_date = now.strftime("%d %B, %Y")  # 15 August, 2026
current_time = now.strftime("%I:%M %p")   # 06:39 PM

# System instruction with real date/time
system_instruction = f"""
তুমি এজন অসমীয়া AI সহায়ক। 
আজিৰ তাৰিখ: {current_date}
এতিয়াৰ সময়: {current_time}
সময় অসম/ভাৰতৰ সময় অনুসৰি।
যদি কোনোবাই তাৰিখ বা সময় সোধে, ওপৰ তথ্য ব্যৱহাৰ কৰি উত্তৰ দিয়া।
সদায় অসমীয়াত উত্তৰ দিবা।
"""

# Initialize chat
model = genai.GenerativeModel('gemini-3.6-flash'),
    system_instruction=system_instruction
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("ইয়াত লিখক..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("চিন্তা কৰি আছো..."):
            response = model.generate_content(prompt)
            answer = response.text
            st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
