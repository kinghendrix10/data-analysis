# frontend/utils/ui_components.py

import streamlit as st
import requests
import plotly.graph_objs as go

def chatbot_greeting():
    st.write("Welcome to the Data Analysis App! You can upload a file or ask a question to begin your analysis.")

def file_upload_component():
    uploaded_file = st.file_uploader("Upload File", type=["xlsx", "csv"])
    if uploaded_file is not None:
        try:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            response = requests.post("http://localhost:8000/upload", files=files, timeout=10)
            response.raise_for_status()
            
            st.session_state["uploaded_file"] = uploaded_file
            st.success(f"File '{uploaded_file.name}' uploaded successfully.")
            st.session_state.messages.append({
                "role": "assistant", 
                "content": f"Great! I've received your file '{uploaded_file.name}'. What kind of analysis or visualization would you like me to perform on this data?"
            })
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to upload file: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
    return uploaded_file

def display_chat_message(msg):
    with st.chat_message(msg['role']):
        st.write(msg['content'])

def display_visualization(visualization_data):
    if isinstance(visualization_data, go.Figure):
        st.plotly_chart(visualization_data)
    elif isinstance(visualization_data, dict):
        # Assume it's a Plotly figure dict
        fig = go.Figure(visualization_data)
        st.plotly_chart(fig)
    else:
        st.error("Unsupported visualization data format")

def display_data_summary(data):
    st.write("## Data Summary")
    st.write(data.describe())
    st.write("### First few rows of the data:")
    st.write(data.head())

def display_code_snippet(code):
    st.code(code)