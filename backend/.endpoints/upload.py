from fastapi import APIRouter, UploadFile, File
import pandas as pd
from ..utils.excel_parsing import parse_excel_file

router = APIRouter()

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    try:
        df = parse_excel_file(file.file)
        # Save or process the dataframe as needed
        return {"status": "success", "message": "File uploaded successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
