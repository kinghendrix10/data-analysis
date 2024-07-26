# backend/services/file_processing.py

from fastapi import UploadFile
import pandas as pd
import io

async def process_upload(file: UploadFile):
    content = await file.read()
    df = pd.read_excel(io.BytesIO(content))
    # Save or process the dataframe as needed
    return {"message": "File uploaded successfully"}
