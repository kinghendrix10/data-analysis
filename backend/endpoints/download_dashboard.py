from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/")
async def download_dashboard(filename: str):
    try:
        file_path = os.path.join("saved_dashboards", filename)
        return FileResponse(file_path)
    except Exception as e:
        return {"status": "error", "message": str(e)}
