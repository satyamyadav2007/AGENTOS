import streamlit as st
import requests
# ---------------- CONFIG ----------------
BACKEND_URL = "http://127.0.0.1:8000/run"

st.set_page_config(
    page_title="AgentOS",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AgentOS")
st.caption("Autonomous AI Agent Platform (Phase-2)")

# ---------------- SESSION MEMORY ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.chat:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
prompt = st.chat_input("Give your agent a task...")

if prompt:
    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat.append({
        "role": "user",
        "content": prompt
    })

    # Send to backend
    with st.chat_message("assistant"):
        with st.spinner("AgentOS is thinking..."):
            try:
                payload = {
                    "user_id": "streamlit_user",
                    "task": prompt
                }

                response = requests.post(BACKEND_URL, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("response", str(data))

                    st.markdown(reply)
                    st.session_state.chat.append({
                        "role": "assistant",
                        "content": reply
                    })
                else:
                    st.error(f"Backend Error: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Backend not running. Start FastAPI first.")