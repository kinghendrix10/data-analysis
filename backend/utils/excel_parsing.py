import pandas as pd
from io import BytesIO

def parse_excel_file(file: BytesIO):
    df = pd.read_excel(file)
    df.to_csv(f"uploaded_files/{file.filename}.csv", index=False)  # Save for later use
    return df
