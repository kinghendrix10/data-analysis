# data_analysis_app/agents/code_agent.py

import os
import tempfile
from models.llama_model import LlamaModel
from utils.file_processor import get_unique_filename
import subprocess
import sys
import streamlit as st
import pandas as pd
import altair as alt

class CodeAgent:
    def __init__(self):
        self.model = LlamaModel()
        self.max_attempts = 3

    def generate_code(self, intent, file_analysis, code=None, error_message=None, attempt=1):
        # Read requirements.txt
        with open('requirements.txt', 'r') as req_file:
            requirements = req_file.read()

        # Determine the type of output based on the intent
        output_type = 'table' if 'table' in intent.get('visualization', '').lower() else 'visualization'

        prompt = f"""You are a python developer working on a data analysis project.
        Go straight to the point and generate a python script for the following data analysis task:
        Intent: {intent['intent']}
        Analysis type: {intent['analysis type']}
        Output type: {output_type}
        Requirements: {intent['requirements']}
        Fields needed: {intent['fields needed']}
        Code: {code}

        File structure:
        Columns: {file_analysis['columns']}
        Data types: {file_analysis['data_types']}
        Sample data: {file_analysis['sample']}
        
        The data will be loaded from a CSV file named 'temp_data.csv'.

        Identify the Fields needed to perform the requuired task from the File structure: Include code for data preprocessing and analysis.
        {"End the code with a line to display full width interactive graphs or plot or charts using Vega-Altair with st.altair_chart." if output_type == 'visualization' else "End the code with a line to display dataframes with st.dataframe"}
        Provide only the Python code without any introductions, explanations, comments, or markdown formatting.
        When filtering or searching for strings use a like and wildcard search function to find words that contain the search term or terms as requested.
        Also, note that some tasks may require you to filter data based on multiple conditions.
        when doing any kind of graphs/chart or plots do not rename any of the axes.
        Ensure to include all necessary imports at the beginning of the script from the following requirements:{requirements}.
        Do not rush to complete the task, take your time to ensure the code and script are correct and complete for the intended purpose of the analysis task.
        Assume the script will be executed and all the contents of the script are correct programmatically.
        Provide only the Python code without any introductions, explanations, comments, or markdown formatting, your first line must be your "import" commands.
        Do not call st.write or st.markdown or st.set_page_config() in the code.
        """

        if error_message:
            prompt += f"""\nThe code generated an error. Please fix the following error and regenerate the code:\n{error_message}
            Do not rush to complete the task, take your time to ensure the code and script are correct and complete for the intended purpose of the analysis task.
            Assume the script will be executed and all the contents of the script are correct programmatically.
        """

        code = self.model.generate(prompt)
        if code:
            # Remove any potential markdown formatting
            code = code.replace('```python', '').replace('```', '').strip()
            code_lines = code.split('\n')
            filtered_lines = []

            # Flag to start including lines after the first 'import' line is found
            start_including = False

            for line in code_lines:
                if line.startswith('import'):
                    start_including = True
                if start_including:
                    filtered_lines.append(line)

            code = '\n'.join(filtered_lines).strip()

            print(code)

            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(code)
                temp_file_name = temp_file.name

            try:
                # Try to execute the code
                subprocess.run([sys.executable, temp_file_name], 
                                        capture_output=True, text=True, check=True)
                print("Code executed successfully")
 
                # If execution is successful, write to the final destination
                final_file_name = get_unique_filename('generated_files/generated_code/generated_analysis.py')
                os.makedirs(os.path.dirname(final_file_name), exist_ok=True)
                with open(final_file_name, 'w') as f:
                    f.write(code) 
                    print (f"Code written to {final_file_name}")
                    print(f"Output type: {output_type}")
                return final_file_name, output_type
            except subprocess.CalledProcessError as e:
                error_message = f"{e.output}\n{e.stderr}\n{e.stdout}\n{e.returncode})"
                print(f"Error executing code: {error_message}")
                if attempt < self.max_attempts:
                    print(f"Attempting to regenerate code (Attempt {attempt + 1})")
                    return self.generate_code(intent, file_analysis, code, error_message, attempt + 1)
                else:
                    print("Max attempts reached. Unable to generate correct code.")
                    print(f"Last generated code:\n{code}") 
                    return None, None
            finally:
                # Clean up the temporary file
                os.unlink(temp_file_name)

        print("Failed to generate code")
        return None, None

    def render_visualization(self, render_result):
        try:
            exec(render_result)
            return True
        except Exception as e:
            st.error(f"Error rendering: {str(e)}")
            return False