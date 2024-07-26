# frontend/utils/ui_components.py

import streamlit as st
from streamlit.components.v1 import html

def chatbot_greeting():
    html_content = open("templates/chatbot_greeting.html").read()
    st.markdown(html_content, unsafe_allow_html=True)

def file_upload_component():
    html_content = open("templates/file_upload.html").read()
    st.markdown(html_content, unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a file")
    return uploaded_file

def display_chat_message(msg):
    st.write(f"**{msg['role']}:** {msg['content']}")

def display_visualization(visualization_data):
    st.plotly_chart(visualization_data)
