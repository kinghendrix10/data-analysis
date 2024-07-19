from fastapi import APIRouter
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

router = APIRouter()

class Query(BaseModel):
    query: str

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_python_code(query: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate a Python code snippet for the following query: {query}"}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return str(e)

@router.post("/")
async def submit_query(query: Query):
    try:
        generated_code = generate_python_code(query.query)
        exec_globals = {}
        exec(generated_code, exec_globals)
        result = exec_globals.get("result", "No result returned from the code.")
        return {"status": "success", "answer": result, "code": generated_code}
    except Exception as e:
        return {"status": "error", "message": str(e)}
