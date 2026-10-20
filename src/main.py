from fastapi import FastAPI
from src.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

@app.get("/")
def root():
    return {"status": "online", "system": "Smart CRM - Subsystem L02 Warranty Reception"}
