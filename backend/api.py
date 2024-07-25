from fastapi import FastAPI
from backend.endpoints import upload, query, visualization, code, documents, save_dashboard, download_dashboard

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(query.router, prefix="/query", tags=["query"])
app.include_router(visualization.router, prefix="/visualization", tags=["visualization"])
app.include_router(code.router, prefix="/code", tags=["code"])
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(save_dashboard.router, prefix="/save_dashboard", tags=["save_dashboard"])
app.include_router(download_dashboard.router, prefix="/download_dashboard", tags=["download_dashboard"])
