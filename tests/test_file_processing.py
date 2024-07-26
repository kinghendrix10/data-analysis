# tests/test_file_processing.py

import pytest
from backend.services.file_processing import process_upload

@pytest.mark.asyncio
async def test_process_upload():
    file = UploadFile(filename="test.xlsx", file=open("test.xlsx", "rb"))
    response = await process_upload(file)
    assert response["message"] == "File uploaded successfully"
