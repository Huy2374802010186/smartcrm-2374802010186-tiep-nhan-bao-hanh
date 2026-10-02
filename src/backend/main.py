from fastapi import FastAPI

app = FastAPI(title="Smart CRM - L02 Warranty API")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "FastAPI environment is running"}
