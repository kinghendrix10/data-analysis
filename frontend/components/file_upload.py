import streamlit as st
import requests

def file_upload_component():
    uploaded_file = st.file_uploader("Drag and drop file here", type=["xlsx"], label_visibility='collapsed')
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post("http://localhost:8000/upload", files=files)  # Ensure 'localhost' is used
        if response.status_code == 200:
            st.success("File uploaded successfully")
        else:
            st.error("Failed to upload file")
