# data_analysis_app/app.py

import streamlit as st
from agents.interface_agent import InterfaceAgent
from agents.code_agent import CodeAgent
from agents.visualization_agent import VisualizationAgent
from utils.file_processor import FileProcessor
import pandas as pd
import os

st.set_page_config(page_title="Data Analysis App", layout="wide")

def main():
    print("Starting the main function")
    st.title("Data Analysis App")

    interface_agent = InterfaceAgent()
    code_agent = CodeAgent()
    visualization_agent = VisualizationAgent()
    file_processor = FileProcessor()

    data = None
    file_analysis = None

    uploaded_file = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx", "pdf"])

    if uploaded_file:
        print(f"File uploaded: {uploaded_file.name}")
        file_content = uploaded_file.read()
        file_type = uploaded_file.type
        print(f"File type: {file_type}")
        data = file_processor.process_file(file_content, file_type)

        if data is not None:
            st.sidebar.success("File uploaded successfully!")
            file_analysis = interface_agent.analyze_file(data)
            print(f"File analysis: {file_analysis}")

            # Save the uploaded data to a temporary CSV file
            data.to_csv('temp_data.csv', index=False)
            print(f"Data sample:\n{data.head()}")
            print(f"Data saved to temp_data.csv")
        else:
            st.sidebar.error("Error processing file. Please try again.")
            print("Error processing file")
            return

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to analyze?"):
        print(f"User prompt: {prompt}")
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        if file_analysis:
            print("Processing user input")
            is_possible, intent_or_explanation = interface_agent.process_input(prompt, file_analysis)
            print(f"Is request possible: {is_possible}")
            print(f"Intent or explanation: {intent_or_explanation}")
            
            if is_possible:
                print("Generating analysis code")
                # Generate analysis code
                script_path = code_agent.generate_code(intent_or_explanation, file_analysis)
                print(f"Script generated at: {script_path}")
                
                if script_path:
                    print("Executing generated code")
                    # Execute the generated code
                    success, result = visualization_agent.execute_code(script_path)
                    print(f"Code execution result: Success={success}, Result={result}")
                    
                    # Display results
                    with st.chat_message("assistant"):
                        st.markdown("Here's the analysis based on your request:")
                        with open(script_path, 'r') as f:
                            script_content = f.read()
                            print(f"Generated script content:\n{script_content}")
                            st.code(script_content, language="python")
                        st.write(result)
                        if success and os.path.exists('output_plot.png'):
                            print("Visualization generated successfully")
                            st.image('output_plot.png')
                        else:
                            print("No visualization generated")
                            st.write("No visualization was generated. Please check the error message above.")
                    
                    # Clean up temporary files
                    print("Cleaning up temporary files")
                    os.remove(script_path)
                    os.remove('temp_data.csv')
                    if os.path.exists('output_plot.png'):
                        os.remove('output_plot.png')
                    
                    st.session_state.messages.append({"role": "assistant", "content": "Analysis complete. (Code and visualization shown above)"})
                else:
                    print("Failed to generate code")
                    with st.chat_message("assistant"):
                        st.markdown("I'm sorry, I couldn't generate the code for your request. Could you please try again with a different query?")
            else:
                print("Request not possible")
                with st.chat_message("assistant"):
                    st.markdown(intent_or_explanation)
        else:
            print("No file analysis available")
            with st.chat_message("assistant"):
                st.markdown("Please upload a file before asking for analysis.")

if __name__ == "__main__":
    print("Starting the application")
    main()