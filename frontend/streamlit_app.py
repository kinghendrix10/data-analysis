# frontend/streamlit_app.py

import streamlit as st
from utils.ui_components import chatbot_greeting, file_upload_component, display_chat_message, display_visualization, display_data_summary, display_code_snippet
import requests
import os
from dotenv import load_dotenv
import openai
import pandas as pd

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initial setup
st.set_page_config(page_title="Data Analysis App", layout="wide")
st.title("Data Analysis App")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    chatbot_greeting()
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Display chat messages
for message in st.session_state.messages:
    display_chat_message(message)

# File upload component
uploaded_file = file_upload_component()

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    display_chat_message({"role": "user", "content": prompt})
    
    client = openai.OpenAI(api_key=openai_api_key)
    
    try:
        if st.session_state.uploaded_file:
            system_message = f"You are a data analysis AI assistant. A file named '{st.session_state.uploaded_file.name}' has been uploaded. Analyze the user's request in this context."
        else:
            system_message = "You are a data analysis AI assistant. The user hasn't uploaded any file yet."
        
        messages = [{"role": "system", "content": system_message}] + st.session_state.messages
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or another available model
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        display_chat_message({"role": "assistant", "content": assistant_message})
        
        # Simulating data analysis and visualization
        if "visualization" in prompt.lower() and st.session_state.uploaded_file:
            # This is a placeholder. In a real scenario, you'd process the file and create actual visualizations
            df = pd.read_excel(st.session_state.uploaded_file)  # or pd.read_csv for CSV files
            display_data_summary(df)
            
            # Placeholder visualization
            import plotly.express as px
            fig = px.scatter(df.iloc[:, :2], x=df.columns[0], y=df.columns[1])
            display_visualization(fig)
        
        if "code" in prompt.lower():
            # Placeholder code snippet
            code_snippet = """
            import pandas as pd
            import plotly.express as px

            df = pd.read_excel('your_file.xlsx')
            fig = px.scatter(df, x='column1', y='column2')
            fig.show()
            """
            display_code_snippet(code_snippet)
    
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        st.session_state.messages.append({"role": "assistant", "content": error_message})
        display_chat_message({"role": "assistant", "content": error_message})