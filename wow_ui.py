import streamlit as st
import requests

st.set_page_config(page_title="AgentOS Demo", layout="wide")

st.title("🧠 AgentOS — Autonomous AI Agent")

# Input box
task_input = st.text_area(
    "Give a business task to the AI Agent",
    "Find latest AI agent startups, analyze them and suggest best investment"
)

if st.button("🚀 Run Autonomous Agent"):
    with st.spinner("Agent thinking..."):
        try:
            # --- FIX: Changed keys to match your backend ---
            # Backend wants "task" and "user_id", NOT "query" and "user"
            payload = {
                "task": task_input,
                "user_id": "Admin"
            }
            
            response = requests.post(
                "http://127.0.0.1:8000/run", 
                json=payload
            )

            if response.status_code == 200:
                result = response.json()
                st.success("Task Completed")

                # --- Output ---
                st.markdown("### 🤖 Agent Output")
                # Using .get() to avoid crashing
                st.write(result.get("output", result.get("response", "No text returned")))

                # --- Memory ---
                st.markdown("### 🧠 Memory Used")
                st.json(result.get("memory", result.get("messages", "No memory returned")))
            
            else:
                # Show the exact error from the backend if it fails
                st.error(f"Backend Error: {response.status_code}")
                st.code(response.text)

        except Exception as e:
            st.error(f"Connection Error: {e}")
            st.info("Make sure 'uvicorn main:app --reload' is running!")