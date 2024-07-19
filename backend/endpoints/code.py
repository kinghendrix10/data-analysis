from fastapi import APIRouter
from ..utils.nlp import get_code_snippets

router = APIRouter()

@router.get("/")
async def get_code():
    try:
        code_snippets = get_code_snippets()
        return {"status": "success", "code_snippets": code_snippets}
    except Exception as e:
        return {"status": "error", "message": str(e)}
