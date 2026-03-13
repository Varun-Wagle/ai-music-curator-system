from fastapi import FastAPI
from backend.app.database.db import engine

app = FastAPI(
    title="AI Music Curator System",
    description="AI-powered playlist curation backend",
    version="1.0"
)

@app.get("/")
def root():
    return {"message": "AI Music Curator API Running"}

@app.get("/db-test")
def test_db():
    try:
        connection = engine.connect()
        return {"message": "Database connected successfully"}
    except:
        return {"error": "Database connection failed"}