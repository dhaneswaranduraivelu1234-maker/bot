import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



import streamlit as st
from app.rag_pipeline import ask_question

st.set_page_config(page_title="NITT Chatbot", page_icon="🎓", layout="centered")

# ---------- Header ----------
st.title("🎓 NIT Trichy Chatbot")
st.markdown(
    "Ask questions based only on **official NITT website information**."
)

# ---------- Session memory ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- Chat history display ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- User input ----------
question = st.chat_input("Ask something about NIT Trichy...")

if question:
    # show user message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # get bot answer safely
    try:
        answer = ask_question(question)
    except Exception:
        answer = "Sorry, something went wrong. Please try another NITT-related question."

    # show bot message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
