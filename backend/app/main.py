from fastapi import FastAPI
from backend.app.database.db import Base, engine
from backend.app.database import models
from backend.app.api.routes import submission

# Initialize FastAPI app
app = FastAPI(
    title="AI Music Curator System",
    description="AI-powered playlist curation backend",
    version="1.0"
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Register routes
app.include_router(submission.router)

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