# Data Analysis Web Application

## Description
A web application that allows users to upload Excel files, query data using natural language, and visualize results through interactive charts and graphs.

## Technologies Used
- Streamlit (Frontend)
- FastAPI (Backend)
- Pandas, Numpy (Data Analysis)
- Matplotlib, Seaborn, Plotly (Visualization)
- GPT-4o (Intent Understanding)

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Run the backend server: `uvicorn backend.api.main:app --reload`
3. Run the frontend app: `streamlit run frontend/streamlit_app.py`

## Features
- File Upload
- Natural Language Query Processing
- Data Analysis and Visualization
- Code Viewing and Editing
- Conversation History Management
