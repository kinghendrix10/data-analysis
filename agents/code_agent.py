# data_analysis_app/agents/code_agent.py

from models.llama_model import LlamaModel
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO
import ast

class CodeAgent:
    def __init__(self):
        self.model = LlamaModel()

    def generate_code(self, intent, data):
        prompt = f"""
        Generate Python code for the following data analysis task:
        Intent: {intent['intent']}
        Analysis type: {intent['analysis type']}
        Visualization: {intent['visualization']}

        The data is available as a pandas DataFrame named 'data'.
        Include code for data preprocessing, analysis, and visualization using matplotlib or seaborn.
        """

        code = self.model.generate(prompt)
        return code.strip()

    def execute_code(self, code, data):
        # Create a string buffer to capture print output
        output_buffer = StringIO()

        # Create a new figure for matplotlib
        plt.figure()

        # Execute the generated code
        try:
            exec(code, {'data': data, 'pd': pd, 'plt': plt, 'sns': sns, 'print': lambda x: output_buffer.write(str(x) + '\n')})
            
            # Get the printed output
            result = output_buffer.getvalue()

            # Get the current figure if a plot was generated
            if plt.gcf().get_axes():
                visualization = plt.gcf()
            else:
                visualization = None

            plt.close()  # Close the figure to free up memory

            return result, visualization
        except Exception as e:
            return f"Error executing code: {str(e)}", None
