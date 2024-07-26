# tests/test_query_processing.py

import pytest
from backend.services.query_processing import process_query

@pytest.mark.asyncio
async def test_process_query():
    query = "Show me the statistics of the data."
    response = await process_query(query)
    assert response["response"] is not None
