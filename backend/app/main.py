from fastapi import FastAPI
from backend.app.database.db import Base, engine
from backend.app.database import models
from backend.app.api.routes import submission
from backend.app.services.audio_analysis import analyze_audio
from backend.app.api.routes import analysis

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
app.include_router(analysis.router)

@app.get("/")
def root():
    return {"message": "AI Music Curator API Running"}

@app.get("/analyze-test")
def analyze_test():
    """
    Test audio analysis using a sample file.
    """

    file_path = "data/uploads/Lil Nas X - Old Town Road (ft. Billy Ray Cyrus).mp3"

    features = analyze_audio(file_path)

    return features

@app.get("/db-test")
def test_db():
    try:
        connection = engine.connect()
        return {"message": "Database connected successfully"}
    except:
        return {"error": "Database connection failed"}
    
