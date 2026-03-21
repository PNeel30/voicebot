#!/bin/bash
python app/ingest.py
uvicorn app.main:app --reload &
streamlit run streamlit_app.py
