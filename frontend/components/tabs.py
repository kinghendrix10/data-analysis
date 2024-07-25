from components.file_upload import file_upload_component
from components.chat_interface import chat_interface_component
from components.data_visualization import data_visualization_component
import streamlit as st
import requests

def overview_tab():
    st.header("Overview")
    st.write("Welcome to the Interactive Data Analysis Platform")
    data_visualization_component()

def dashboards_tab():
    st.header("Dashboards")
    st.write("This section will display interactive dashboards.")

def code_tab():
    st.header("Generated Code Snippets")
    response = requests.get("http://localhost:8000/code")
    if response.status_code == 200:
        code_snippets = response.json()
        for snippet in code_snippets:
            st.code(snippet)
    else:
        st.error("Failed to retrieve code snippets")

def documents_tab():
    st.header("Uploaded Documents")
    file_upload_component()
    response = requests.get("http://localhost:8000/documents")
    if response.status_code == 200:
        documents = response.json()
        for document in documents:
            st.write(document)
    else:
        st.error("Failed to list documents")

def conversations_tab():
    st.header("Previous Conversations")
    response = requests.get("http://localhost:8000/conversations")
    if response.status_code == 200:
        conversations = response.json()
        for convo in conversations:
            st.write(convo)
    else:
        st.error("Failed to retrieve conversations")
