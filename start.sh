#!/bin/bash

# PTT API Startup Script

echo "Starting PTT API Web Service..."
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting server on port 12000..."
uvicorn main:app --host 0.0.0.0 --port 12000 --reload

echo "API Documentation available at: http://localhost:12000/"
echo "Health check: http://localhost:12000/health"
echo "Parse endpoint: http://localhost:12000/parse?title=<torrent_title>"