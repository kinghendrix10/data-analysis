# Data Analysis App

## Overview

The Data Analysis App is a Streamlit-based application that allows users to upload CSV, Excel, or PDF files and perform data analysis through a chat interface. The app uses advanced AI models (Mixtral and LLaMA 2) via the Groq API to understand user intents and generate appropriate data analysis code.

## Features

- File upload support for CSV, Excel, and PDF formats
- Natural language interface for data analysis requests
- Automatic code generation for data analysis tasks
- Visualization generation (bar charts, line charts, scatter plots, etc.)
- AI-powered intent recognition and clarification

## Prerequisites

- Python 3.8+
- Groq API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/data-analysis-app.git
   cd data-analysis-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file
   - Add your Groq API key to the `.env` file

## Configuration

The `config/config.yaml` file contains various configuration options for the app. You can modify these settings to customize the behavior of the application.

## Usage

1. Start the Streamlit app:
   ```
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Upload a data file (CSV, Excel, or PDF) using the sidebar.

4. Use the chat interface to ask questions or request analyses of your data. For example:
   - "Show me a bar chart of sales by region"
   - "Calculate the average revenue for the last 3 months"
   - "Identify outliers in the 'Price' column"

5. The app will generate and execute the appropriate code, displaying the results and any visualizations.

## Project Structure

- `app.py`: Main Streamlit application
- `agents/`: Contains the interface and code generation agents
- `models/`: AI model wrappers (Groq API for Mixtral and LLaMA 2)
- `utils/`: Utility functions for file processing, data analysis, and visualization
- `config/`: Configuration files

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
