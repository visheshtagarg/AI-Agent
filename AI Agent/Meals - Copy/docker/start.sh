#!/bin/sh
set -e

export STREAMLIT_PORT=${STREAMLIT_PORT:-8501}
export API_PORT=${API_PORT:-8000}

streamlit run app/streamlit_app.py --server.port ${STREAMLIT_PORT} --server.address 0.0.0.0 &
uvicorn app.api:app --host 0.0.0.0 --port ${API_PORT}

