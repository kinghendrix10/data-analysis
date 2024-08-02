# data_analysis_app/app.py

import streamlit as st
from agents.interface_agent import InterfaceAgent
from agents.code_agent import CodeAgent
from utils.file_processor import FileProcessor, get_unique_filename
import pandas as pd
import os

st.set_page_config(page_title="Data Analysis App", layout="wide")

def main():
    print("Starting the main function")
    st.title("Data Analysis App")

    interface_agent = InterfaceAgent()
    code_agent = CodeAgent()
    file_processor = FileProcessor()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "file_analysis" not in st.session_state:
        st.session_state.file_analysis = None

    uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx", "pdf"])

    if uploaded_file:
        print(f"File uploaded: {uploaded_file.name}")
        file_content = uploaded_file.read()
        file_type = uploaded_file.type
        print(f"File type: {file_type}")
        data = file_processor.process_file(file_content, file_type)

        if data is not None:
            st.sidebar.success("File uploaded successfully!")
            st.session_state.file_analysis = interface_agent.analyze_file(data)
            print(f"File analysis: {st.session_state.file_analysis}")

            # Display warnings and errors
            if st.session_state.file_analysis['warnings']:
                st.warning("Warnings:")
                for warning in st.session_state.file_analysis['warnings']:
                    st.write(f"- {warning}")
            
            if st.session_state.file_analysis['errors']:
                st.error("Errors:")
                for error in st.session_state.file_analysis['errors']:
                    st.write(f"- {error}")

            # Save the uploaded data to a temporary CSV file
            data.to_csv('temp_data.csv', index=False)
            print(f"Data sample:\n{data.head()}")
            print(f"Data saved to temp_data.csv")
        else:
            st.sidebar.error("Error processing file. Please try again.")
            print("Error processing file")
            return

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "output_type" in message and "output_content" in message:
                    code_agent.render_visualization(message["output_content"])

    if prompt := st.chat_input("What would you like to analyze?"):
        print(f"User prompt: {prompt}")
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if st.session_state.file_analysis:
            print("Processing user input")
            is_possible, intent_or_explanation = interface_agent.process_input(prompt, st.session_state.file_analysis)
            print(f"Is request possible: {is_possible}")
            print(f"Intent or explanation: {intent_or_explanation}")
            
            if is_possible:
                print("Generating analysis code")
                script_path, output_type = code_agent.generate_code(intent_or_explanation, st.session_state.file_analysis)
                
                if script_path:
                    print(f"Script generated at: {script_path}")
                    print(f"Output type: {output_type}")
                    
                    # Display results
                    with st.chat_message("assistant"):
                        st.markdown("Here's the analysis based on your request:")
                        with open(script_path, 'r') as f:
                            script_content = f.read()
                            print(f"Generated script content:\n{script_content}")
                            st.code(script_content, language="python")
                        st.write('Analysis executed successfully.')
                        if script_content:
                                print("Rendering visualization")
                                output_content = code_agent.render_visualization(script_content)
                                print (f"Output content: {output_content}")
                        else:
                            st.write("No visualization or table was generated. Please check the error message above.")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Analysis complete. Code:\n```python\n{script_content}\n```",
                        "output_type": output_type,
                        "output_content": output_content
                    })

                    # Clean up temporary files
                    if os.path.exists('temp_data.csv'):
                        os.remove('temp_data.csv')
                        print("Temporary data file removed")
                    else:
                        print("Script path is None")
                        st.write("Failed to generate code. Please try again with a different query.")
                else:
                    print(f"Unexpected generation result")
                    st.write("An error occurred during code generation. Please try again.")
            else:
                print("Request not possible")
                with st.chat_message("assistant"):
                    st.markdown(intent_or_explanation)
                    st.markdown("Would you like to try a different analysis?")
        else:
            print("No file analysis available")
            with st.chat_message("assistant"):
                st.markdown("Please upload a file to begin analysis.")

if __name__ == "__main__":
    print("Starting the application")
    main()