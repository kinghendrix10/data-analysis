# backend/services/query_processing.py

from ..models.intent_model import deduce_intent
from .data_analysis import perform_analysis

async def process_query(query: str):
    intent = deduce_intent(query)
    if intent["status"] == "clear":
        analysis_result = perform_analysis(intent["data"])
        return {"response": analysis_result}
    elif intent["status"] == "unclear":
        return {"response": "Could you please clarify your request?"}
    else:
        return {"response": "The request cannot be processed. Try a different query."}
