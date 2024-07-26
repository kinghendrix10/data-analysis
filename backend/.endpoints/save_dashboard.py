from fastapi import APIRouter, Body
from ..utils.visualization import save_dashboard

router = APIRouter()

@router.post("/")
async def save_dashboard_route(data: dict = Body(...)):
    try:
        save_dashboard(data)
        return {"status": "success", "message": "Dashboard saved successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
