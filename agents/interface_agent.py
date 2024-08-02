# data_analysis_app/agents/interface_agent.py

from models.mixtral_model import MixtralModel
import pandas as pd

class InterfaceAgent:
    def __init__(self):
        self.model = MixtralModel()

    def analyze_file(self, data):
        columns = data.columns.tolist()
        data_types = data.dtypes.to_dict()
        sample = data.head().to_dict()
        
        prompt = f""" You are a data analyst working on a data analysis project.
        Analyze the following dataset structure and provide insights:
        
        Columns: {columns}
        Data types: {data_types}
        Sample data: {sample}
        
        Please identify any potential errors or warnings in the data structure.
        Consider issues such as:
        - Numeric columns stored as strings
        - Date parsing issues
        - Future dates
        - Missing values
        - High-cardinality categorical variables
        
        Provide your analysis in the following format:
        Errors: [List of identified errors]
        Warnings: [List of potential issues or warnings]
        Your analysis should be summarized in the shortest possible way to convey the information. 
        """
        
        analysis = self.model.generate(prompt)
        
        return {
            "columns": columns,
            "data_types": {str(k): str(v) for k, v in data_types.items()},
            "sample": sample,
            **self._parse_analysis(analysis)
        }

    def _parse_analysis(self, analysis):
        lines = analysis.strip().split('\n')
        result = {"errors": [], "warnings": []}
        current_section = None
        for line in lines:
            if line.startswith("Errors:"):
                current_section = "errors"
            elif line.startswith("Warnings:"):
                current_section = "warnings"
            elif current_section and line.strip():
                result[current_section].append(line.strip())
        return result


    def process_input(self, user_input, file_analysis):
        prompt = f""" You are a data analyst working on a data analysis project.
        Analyze the following user input and file structure to determine if the request is possible:
        
        User input: {user_input}
        
        File structure:
        Columns: {file_analysis['columns']}
        Data types: {file_analysis['data_types']}
        Sample data: {file_analysis['sample']}
        
        Errors: {file_analysis['errors']}
        Warnings: {file_analysis['warnings']}
        
        Provide the intent in the following format:
        Intent: [brief description of the intent]
        Analysis type: [e.g., descriptive, comparative, predictive]
        Visualization: [type of visualization if applicable, e.g., bar chart, scatter plot, table, etc.]
        Requirements:[any specific requirements or constraints eg last 3 months, all data, top 10 data, etc]
        Fields needed: [list of fields needed for the analysis]
        
        If the request is not possible with the given data, explain why and suggest an alternative analysis.
        Take your time to ensure your analysis is correct and complete for the intended purpose.
        """

        response = self.model.generate(prompt)
        
        # Parse the response
        intent_lines = response.strip().split('\n')
        intent = {}
        is_possible = True

        for line in intent_lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key, value = parts
                    intent[key.strip().lower()] = value.strip()

        if 'intent' not in intent or 'analysis type' not in intent or 'visualization' not in intent:
            is_possible = False
            intent_or_explanation = response

        return is_possible, intent if is_possible else intent_or_explanation

    def clarify_intent(self, user_input, file_analysis):
        prompt = f"""
        The user's request "{user_input}" needs clarification:
        
        File structure:
        Columns: {file_analysis['columns']}
        Data types: {file_analysis['data_types']}
        Sample data: {file_analysis['sample']}
        
        Errors: {file_analysis['errors']}
        Warnings: {file_analysis['warnings']}
        
        Generate a clarifying question or suggest an alternative analysis based on the available data.
        """

        clarification = self.model.generate(prompt)
        return clarification.strip()