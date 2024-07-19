import streamlit as st
from components.file_upload import file_upload_component
from components.chat_interface import chat_interface_component
from components.data_visualization import data_visualization_component
from components.tabs import overview_tab, dashboards_tab, code_tab, documents_tab
from dotenv import load_dotenv
import openai
import os

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Data Analysis Platform", layout="wide")  
# st.title("Interactive Data Analysis Platform")

tabs = ["Overview", "Dashboards", "Code Snippets", "Documents"]
selected_tab = st.sidebar.selectbox("Navigate", tabs)

if selected_tab == "Overview":
    overview_tab()
elif selected_tab == "Dashboards":
    dashboards_tab()
elif selected_tab == "Code Snippets":
    code_tab()
elif selected_tab == "Documents":
    documents_tab()


# with st.sidebar:
#     st.overview_tab()
#     # ["Dashboards"]dashboards_tab()
#     # ["Code Snippets"]
#     # ["Documents"]



import streamlit as st

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# st.title("💬 Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = openai.OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)