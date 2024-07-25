import streamlit as st
import requests

def file_upload_component():
    uploaded_file = st.file_uploader("Upload File", type=["xlsx"])
    if uploaded_file is not None:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        response = requests.post("http://localhost:8000/upload", files=files)
        if response.status_code == 200:
            st.session_state["uploaded_file"] = uploaded_file
            st.success(f"File '{uploaded_file.name}' uploaded successfully.")
            st.write("What kind of visuals would you like to see from this data?")
        else:
            st.error("Failed to upload file")
