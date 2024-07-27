# data_analysis_app/models/llama_model.py

import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM

load_dotenv()

class LlamaModel:
    def __init__(self):
        model_path = os.getenv("LLAMA_MODEL_PATH")
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)

    def generate(self, prompt, max_length=1000):
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt")
            outputs = self.model.generate(**inputs, max_length=max_length)
            return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        except Exception as e:
            print(f"Error in LLaMA model generation: {str(e)}")
            return None
