import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

class SonnetModel:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-5-sonnet-20240620"

    def generate(self, prompt, max_tokens=1000):
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system="You are a helpful AI assistant for data analysis and code generation.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response["content"][0]["text"]
        except Exception as e:
            print(f"Error in Anthropic API call: {str(e)}")
            return None