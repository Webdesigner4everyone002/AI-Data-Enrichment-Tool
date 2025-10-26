# app.py
import streamlit as st
import pandas as pd
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
import asyncio

from search_api import search_entity
from llm_agent import extract_info

# Load environment variables
load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_API_CREDENTIALS")

st.title("AI Data Enrichment Tool")

# --- 1) Upload CSV ---
uploaded_file = st.file_uploader("Upload CSV file", type="csv")
df = None
column = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of your CSV:")
    st.dataframe(df.head())
    column = st.selectbox("Select the main column for search", df.columns)

# --- 2) Connect Google Sheet ---
use_sheet = st.checkbox("Connect to Google Sheet instead")
sheet_id = None
service = None

if use_sheet:
    creds = Credentials.from_service_account_file(
        GOOGLE_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    sheet_id = st.text_input("Enter Google Sheet ID")
    if sheet_id:
        service = build("sheets", "v4", credentials=creds)
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, range="Sheet1"
        ).execute()
        values = result.get("values", [])
        if values:
            df = pd.DataFrame(values[1:], columns=values[0])
            st.write("Preview of your Google Sheet:")
            st.dataframe(df.head())
            column = st.selectbox("Select the main column for search", df.columns)

# --- 3) Prompt template ---
prompt_template = st.text_input(
    "Enter the prompt template (use {entity} as placeholder)",
    "Find the email address of {entity}"
)

# --- 4) Checkbox for updating Google Sheet ---
update_sheet = st.checkbox("Update Google Sheet with results")

# --- 5) Async enrichment functions ---
async def enrich_entity(entity, prompt_template, semaphore):
    async with semaphore:
        snippets = await asyncio.to_thread(search_entity, entity, prompt_template)
        info = await asyncio.to_thread(extract_info, entity, prompt_template, snippets)
        return {"entity": entity, "extracted_info": info}

async def run_enrichment(entities, prompt_template, concurrency=3):
    semaphore = asyncio.Semaphore(concurrency)
    tasks = [enrich_entity(e, prompt_template, semaphore) for e in entities]
    results = []
    for f in asyncio.as_completed(tasks):
        res = await f
        results.append(res)
    return results

# --- 6) Start enrichment button ---
if df is not None and column is not None:
    if st.button("Start Enrichment"):
        entities = df[column].astype(str).tolist()
        result_df = asyncio.run(run_enrichment(entities, prompt_template, concurrency=3))
        result_df = pd.DataFrame(result_df)
        st.success("Enrichment complete!")
        st.dataframe(result_df)

        # Download CSV
        csv = result_df.to_csv(index=False)
        st.download_button("Download Results as CSV", csv, "results.csv")

        # Update Google Sheet if checkbox selected
        if update_sheet and use_sheet and sheet_id and service is not None:
            new_column = "Extracted Info"
            df[new_column] = result_df['extracted_info']
            service.spreadsheets().values().update(
                spreadsheetId=sheet_id,
                range="Sheet1!A1",
                valueInputOption="RAW",
                body={"values": [df.columns.tolist()] + df.values.tolist()}
            ).execute()
            st.success("Google Sheet updated with extracted info!")
