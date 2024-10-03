#!/bin/bash
# Lancer l'application FastAPI
uvicorn main:app --host 0.0.0.0 --reload --port 8000
