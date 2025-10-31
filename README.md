# EnrichIQ —-- LangChain-Powered AI Data Enrichment Dashboard

A Streamlit-based dashboard that allows users to upload CSV files or connect Google Sheets, perform web searches for each entity in a selected column, and extract specific information using an LLM (Google Gemini API via LangChain). Extracted results can be viewed, downloaded, or updated directly in Google Sheets.

# Features

Upload CSV or connect to Google Sheets for input data.

Preview uploaded data and select the main column for enrichment.

Dynamic prompt template input (use {entity} placeholder).

Automated web search for each entity (via SerpAPI).

LLM-powered information extraction using Google Gemini API.

Asynchronous processing for faster enrichment.

Display results in a table.

# Tech Stack

| Layer           | Technology/Tool                 |
| --------------- | ------------------------------- |
| Frontend/UI     | Streamlit                       |
| Data Handling   | pandas, Google Sheets API       |
| Search API      | SerpAPI                         |
| LLM API         | Google Gemini API via LangChain |
| Backend         | Python                          |
| Agents/Workflow | LangChain                       |
| Retry Mechanism | tenacity                        |

# Installation

Clone the repository:
git clone <repo_url>
cd ai_data_enrichment

Create and activate virtual environment:
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

Install dependencies:
pip install -r requirements.txt

Set environment variables (create .env file in project root):
SERPAPI_API_KEY=your_serpapi_key
GEMINI_API_KEY=your_gemini_key
GOOGLE_API_CREDENTIALS=path_to_your_service_account.json

Running the App
streamlit run app.py

Access the dashboard at http://localhost:8501.

Upload a CSV file or connect a Google Sheet.

Select the main column for enrichment.

Enter a prompt template (e.g., Find the email address of {entity}).

Click Start Enrichment.

Once complete, view results, download as CSV, or update Google Sheet.

# Folder Structure 
ai_data_enrichment/
├─ app.py                  # Streamlit dashboard
├─ search_api.py           # SerpAPI search wrapper with retries
├─ llm_agent.py            # LLM extraction wrapper via LangChain
├─ requirements.txt        # Python dependencies
├─ .env                    # Environment variables (API keys)
└─ README.md

Download results as CSV or update Google Sheet directly.

Robust error handling and retry logic for API calls.
