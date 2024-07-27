# data_analysis_app/app.py

import streamlit as st
from agents.interface_agent import InterfaceAgent
from agents.code_agent import CodeAgent
from utils.file_processor import FileProcessor
import os

st.set_page_config(page_title="Data Analysis App", layout="wide")

def main():
    st.title("Data Analysis App")

    # Initialize agents and file processor
    interface_agent = InterfaceAgent()
    code_agent = CodeAgent()
    file_processor = FileProcessor()

    # Sidebar for file upload
    uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx", "pdf"])

    if uploaded_file:
        file_content = uploaded_file.read()
        file_type = uploaded_file.type
        data = file_processor.process_file(file_content, file_type)

        if data is not None:
            st.sidebar.success("File uploaded successfully!")
        else:
            st.sidebar.error("Error processing file. Please try again.")
            return

    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to analyze?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Process user input with interface agent
        intent = interface_agent.process_input(prompt)

        if intent:
            # Generate code with code agent
            code = code_agent.generate_code(intent, data)

            # Execute code and get results
            result, visualization = code_agent.execute_code(code, data)

            # Display results
            with st.chat_message("assistant"):
                st.markdown("Here's the analysis based on your request:")
                st.code(code, language="python")
                st.write(result)
                if visualization:
                    st.pyplot(visualization)

            st.session_state.messages.append({"role": "assistant", "content": f"Analysis complete. Code:\n```python\n{code}\n```"})
        else:
            with st.chat_message("assistant"):
                st.markdown("I'm sorry, I couldn't understand your request. Could you please rephrase it?")
            st.session_state.messages.append({"role": "assistant", "content": "I'm sorry, I couldn't understand your request. Could you please rephrase it?"})

if __name__ == "__main__":
    main()
