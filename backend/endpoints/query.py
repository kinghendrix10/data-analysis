from fastapi import APIRouter, HTTPException, UploadFile, File
from ..utils.nlp import process_query
import openai
import os
import traceback

router = APIRouter()

# Initialize OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

@router.post("/query")
async def query(data: dict):
    query_text = data.get("query")
    if not query_text:
        raise HTTPException(status_code=400, detail="Query text is required")

    try:
        # Process the query to generate Python code
        code = process_query(query_text)

        # Execute the generated code
        local_vars = {}
        exec(code, {}, local_vars)

        # Extract results for visualization
        result = local_vars.get("result", {})
        visualization_data = local_vars.get("visualization_data", {})

        return {
            "status": "success",
            "code": code,
            "result": result,
            "visualization_data": visualization_data
        }
    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        return {
            "status": "error",
            "message": error_msg
        }

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = f"/mnt/data/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        return {"status": "success", "message": f"File '{file.filename}' uploaded successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
