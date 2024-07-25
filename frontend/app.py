import streamlit as st
from components.file_upload import file_upload_component
from components.chat_interface import chat_interface_component
from components.data_visualization import data_visualization_component
from components.tabs import overview_tab, dashboards_tab, code_tab, documents_tab, conversations_tab
from dotenv import load_dotenv
import openai
import os
import requests

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Data Analysis Platform", layout="wide")

tabs = ["Overview", "Chat", "Dashboards", "Documents", "Code", "Conversations"]
selected_tab = st.sidebar.selectbox("Navigate", tabs)

if selected_tab == "Overview":
    overview_tab()
elif selected_tab == "Chat":
    chat_interface_component()
elif selected_tab == "Dashboards":
    dashboards_tab()
elif selected_tab == "Documents":
    documents_tab()
elif selected_tab == "Code":
    code_tab()
elif selected_tab == "Conversations":
    conversations_tab()

# Initialize session state for messages and uploaded file
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome! You can upload a file or ask a question to begin your analysis."}]
if "uploaded_file" not in st.session_state:
    st.session_state["uploaded_file"] = None

# Display chat messages from the session state
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle chat input
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Check if the prompt is an upload request or a regular query
    if "upload" in prompt.lower():
        file_upload_component()
    else:
        response = requests.post("http://localhost:8000/query", json={"query": prompt})
        if response.status_code == 200:
            result = response.json()
            if result["status"] == "success":
                if "answer" in result:
                    st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
                    st.chat_message("assistant").write(result["answer"])
                if "code" in result:
                    st.session_state["code_snippet"] = result["code"]
                    st.code(result["code"])
                if "visualization_data" in result:
                    data_visualization_component(result["visualization_data"])
            else:
                st.session_state.messages.append({"role": "assistant", "content": result.get("message", "Failed to process query")})
                st.chat_message("assistant").write(result.get("message", "Failed to process query"))
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Failed to process query"})
            st.chat_message("assistant").write("Failed to process query")

# Display file upload component separately for file upload process
file_upload_component()

