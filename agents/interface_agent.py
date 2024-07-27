# data_analysis_app/agents/interface_agent.py

from models.groq_model import GroqModel
import pandas as pd

class InterfaceAgent:
    def __init__(self):
        self.model = GroqModel()

    def analyze_file(self, data):
        # Analyze the uploaded file
        columns = data.columns.tolist()
        data_types = data.dtypes.to_dict()
        sample = data.head().to_dict()
        
        return {
            "columns": columns,
            "data_types": {str(k): str(v) for k, v in data_types.items()},
            "sample": sample
        }

    def process_input(self, user_input, file_analysis):
        prompt = f"""
        Analyze the following user input and file structure to determine if the request is possible:
        
        User input: {user_input}
        
        File structure:
        Columns: {file_analysis['columns']}
        Data types: {file_analysis['data_types']}
        Sample data: {file_analysis['sample']}
        
        If the request is possible, provide the intent in the following format:
        Intent: [brief description of the intent]
        Analysis type: [e.g., descriptive, comparative, predictive]
        Visualization: [type of visualization if applicable, e.g., table, bar chart, scatter plot, etc.]
        
        If the request is not possible with the given data, explain why and suggest an alternative analysis.
        """

        response = self.model.generate(prompt)
        
        # Parse the response
        intent_lines = response.strip().split('\n')
        intent = {}
        is_possible = False

        for line in intent_lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key, value = parts
                    intent[key.strip().lower()] = value.strip()

        if 'intent' in intent and 'analysis type' in intent:
            is_possible = True
            if 'visualization' not in intent:
                intent['visualization'] = 'None specified'
        else:
            intent_or_explanation = response

        return is_possible, intent if is_possible else intent_or_explanation

    def clarify_intent(self, user_input, file_analysis):
        prompt = f"""
        The user's request "{user_input}" is unclear or not possible with the given data:
        
        File structure:
        Columns: {file_analysis['columns']}
        Data types: {file_analysis['data_types']}
        Sample data: {file_analysis['sample']}
        
        Generate a clarifying question or suggest an alternative analysis based on the available data.
        """

        clarification = self.model.generate(prompt)
        return clarification.strip()