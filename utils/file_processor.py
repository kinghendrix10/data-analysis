# data_analysis_app/utils/file_processor.py

import pandas as pd
import PyPDF2
import io

class FileProcessor:
    def process_file(self, file_content, file_type):
        if file_type == "text/csv":
            return self._process_csv(file_content)
        elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            return self._process_excel(file_content)
        elif file_type == "application/pdf":
            return self._process_pdf(file_content)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

    def _process_csv(self, file_content):
        try:
            return pd.read_csv(io.StringIO(file_content.decode('utf-8')))
        except Exception as e:
            print(f"Error processing CSV: {str(e)}")
            return None

    def _process_excel(self, file_content):
        try:
            return pd.read_excel(io.BytesIO(file_content))
        except Exception as e:
            print(f"Error processing Excel: {str(e)}")
            return None

    def _process_pdf(self, file_content):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return pd.DataFrame({'text': [text]})
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None
