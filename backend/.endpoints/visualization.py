from fastapi import APIRouter
from ..utils.visualization import generate_visualization

router = APIRouter()

@router.get("/")
async def get_visualization():
    try:
        data = generate_visualization()
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
