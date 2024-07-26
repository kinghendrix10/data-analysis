from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/")
async def list_documents():
    try:
        documents = os.listdir("uploaded_files")
        return {"status": "success", "documents": documents}
    except Exception as e:
        return {"status": "error", "message": str(e)}
