# data_analysis_app/utils/file_processor.py

import os
import pandas as pd
import io
from models.mixtral_model import MixtralModel

class FileProcessor:
    def __init__(self):
        self.model = MixtralModel()

    def process_file(self, file_content, file_type):
        try:
            if file_type == "text/csv":
                df = self._process_csv(file_content)
            elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                df = self._process_excel(file_content)
            elif file_type == "application/pdf":
                df = self._process_pdf(file_content)
            else:
                df = self._process_with_llm(file_content, file_type)
            
            return self._preprocess_dataframe(df)
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return None

    def _process_csv(self, file_content):
        return pd.read_csv(io.StringIO(file_content.decode('utf-8')))

    def _process_excel(self, file_content):
        return pd.read_excel(io.BytesIO(file_content))

    def _process_pdf(self, file_content):
        # You might want to implement a more sophisticated PDF processing method here
        # For now, we'll just return a DataFrame with the raw content
        return pd.DataFrame({'content': [file_content.decode('utf-8', errors='ignore')]})

    def _process_with_llm(self, file_content, file_type):
        processing_instructions = self._get_processing_instructions(file_type)
        return self._execute_processing(file_content, processing_instructions)

    def _get_processing_instructions(self, file_type):
        prompt = f"""
        Provide Python code to process a file of type: {file_type}
        The code should return a pandas DataFrame named 'result_df'.
        Use appropriate libraries (e.g., pandas) and handle potential errors.
        Only provide the Python code, no explanations.
        """
        return self.model.generate(prompt)

    def _execute_processing(self, file_content, instructions):
        exec_globals = {
            'pd': pd,
            'io': io,
            'file_content': file_content,
            'result_df': None
        }
        
        try:
            exec(instructions, exec_globals)
            if exec_globals['result_df'] is None:
                raise ValueError("Processing instructions did not produce a result_df")
            return exec_globals['result_df']
        except Exception as e:
            raise ValueError(f"Error executing processing instructions: {str(e)}")

    def _preprocess_dataframe(self, df):
        prompt = f"""
        Provide Python code to preprocess the following DataFrame:
        
        Columns: {df.columns.tolist()}
        Data types: {df.dtypes.to_dict()}
        
        Consider the following tasks:
        - Convert date columns to datetime
        - Handle missing values
        - Normalize column names
        - Any other necessary preprocessing steps
        
        The code should modify the 'df' variable in place.
        Only provide the Python code, no explanations.
        """
        preprocessing_code = self.model.generate(prompt)
        
        exec_globals = {
            'pd': pd,
            'df': df
        }
        
        try:
            exec(preprocessing_code, exec_globals)
            return exec_globals['df']
        except Exception as e:
            print(f"Error in preprocessing: {str(e)}")
            return df  # Return original dataframe if preprocessing fails

def get_unique_filename(base_name):
    directory = os.path.dirname(base_name)
    filename = os.path.basename(base_name)
    name, ext = os.path.splitext(filename)
    
    os.makedirs(directory, exist_ok=True)
    
    counter = 1
    while os.path.exists(os.path.join(directory, filename)):
        filename = f"{name}({counter}){ext}"
        counter += 1
    
    return os.path.join(directory, filename)