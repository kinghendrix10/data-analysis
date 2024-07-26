# backend/utils/response_formatting.py

import json

def format_response(data):
    return json.dumps(data)
