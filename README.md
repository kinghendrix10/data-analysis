# Interactive Data Analysis Platform

This project is an interactive data analysis platform that allows users to upload Excel files, query data using natural language, and visualize results through interactive charts and graphs.

## Features

- File Upload: Upload Excel files to the platform.
- Natural Language Queries: Submit queries in natural language and get data insights.
- Data Visualization: View data through interactive charts and graphs.
- Code Snippets: Get generated code snippets based on queries.
- Document Management: List and manage uploaded documents.
- Dashboard Saving: Save and download visualizations as dashboards.

## Setup

1. Clone the repository.
2. Install the dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the backend server:
    ```
    uvicorn backend.api:app --reload
    ```
4. Run the Streamlit app:
    ```
    streamlit run frontend/app.py
    ```

## Usage

1. Open the Streamlit app in your browser.
2. Upload an Excel file.
3. Use the chat interface to submit queries.
4. View visualizations and generated code snippets.
5. Manage uploaded documents and save dashboards.

## License

This project is licensed under the MIT License.
