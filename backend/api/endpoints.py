# backend/api/endpoints.py

from fastapi import APIRouter, UploadFile, File
from ..services import file_processing, query_processing

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return await file_processing.process_upload(file)

@router.post("/query")
async def query_data(query: dict):
    return await query_processing.process_query(query["query"])
