# frontend/streamlit_app.py

import streamlit as st
from utils.ui_components import chatbot_greeting, file_upload_component, display_chat_message, display_visualization
import requests

# Initial setup
st.set_page_config(page_title="Data Analysis App", layout="wide", theme="dark")

# Chatbot greeting
chatbot_greeting()

# Chat input and file upload
uploaded_file = file_upload_component()

if uploaded_file:
    response = requests.post('http://localhost:8000/upload', files={"file": uploaded_file})
    if response.status_code == 200:
        st.session_state["uploaded_file"] = response.json()
        st.session_state["messages"].append({"role": "system", "content": "File uploaded successfully."})

# Chatbot interface
user_input = st.text_input("Ask your question or upload a file to begin:")

if user_input:
    response = requests.post('http://localhost:8000/query', json={"query": user_input})
    if response.status_code == 200:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["messages"].append({"role": "bot", "content": response.json()["response"]})

# Display chat messages
for msg in st.session_state.get("messages", []):
    display_chat_message(msg)

# Display visualizations if available
if "visualization" in st.session_state:
    display_visualization(st.session_state["visualization"])
