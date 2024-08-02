# data_analysis_app/models/llama_model.py

import os
from dotenv import load_dotenv
import groq

load_dotenv()

class LlamaModel:
    def __init__(self):
        self.client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama3-70b-8192"

    def generate(self, prompt, max_tokens=1000):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant for data analysis and code generation."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in LLaMA API call: {str(e)}")
            return None