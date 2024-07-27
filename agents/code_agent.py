# data_analysis_app/agents/code_agent.py

import os
from models.llama_model import LlamaModel

class CodeAgent:
    def __init__(self):
        self.model = LlamaModel()

    def generate_code(self, intent, file_analysis):
        prompt = f"""
        Generate Python code for the following data analysis task:
        Intent: {intent['intent']}
        Analysis type: {intent['analysis type']}
        Visualization: {intent['visualization']}
        
        File structure:
        Columns: {file_analysis['columns']}
        Data types: {file_analysis['data_types']}
        Sample data: {file_analysis['sample']}
        
        The data will be loaded from a CSV file named 'temp_data.csv'.
        Include code for data preprocessing, analysis, and visualization using matplotlib.
        The code should save the generated plot as 'output_plot.png' for charts and graphs
        and generated tables as output.csv for tables.
        Provide only the Python code without any explanations, comments, or markdown formatting.
        Ensure to include all necessary imports at the beginning of the script.
        """

        code = self.model.generate(prompt)
        if code:
            # Remove any potential markdown formatting
            code = code.replace('```python', '').replace('```', '').strip()

            # Ensure necessary imports are included
            imports = """
import pandas as pd
import matplotlib.pyplot as plt
import plotly as px
"""
            # Add data loading code
            data_loading = """
# Load data
data = pd.read_csv('temp_data.csv')
"""
            full_code = imports + data_loading + code

            # Write the generated code to a file
            with open('generated_analysis.py', 'w') as f:
                f.write(full_code)
            return 'generated_analysis.py'
        return None