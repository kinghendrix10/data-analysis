from transformers import pipeline

nlp_pipeline = pipeline("text2text-generation")

def process_query(query):
    response = nlp_pipeline(query)
    # Assuming the response is a list of dictionaries
    return response[0]["generated_text"]

def get_code_snippets():
    # Example code snippets
    code_snippets = [
        "import pandas as pd\n\ndf = pd.read_csv('data.csv')\ndf.head()",
        "import matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [4, 5, 6])\nplt.show()"
    ]
    return code_snippets
