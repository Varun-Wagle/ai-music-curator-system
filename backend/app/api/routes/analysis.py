from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.db import get_db
from backend.app.database.models import Song, AudioFeatures
from backend.app.services.audio_analysis import analyze_audio

router = APIRouter()


@router.post("/analyze-song/{song_id}")
def analyze_song(song_id: int, db: Session = Depends(get_db)):

    song = db.query(Song).filter(Song.id == song_id).first()

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    file_path = str(song.file_path)

    features = analyze_audio(file_path)

    audio_features = AudioFeatures(
        song_id=song.id,
        tempo=features["tempo"],
        duration=features["duration"],
        spectral_centroid=features["spectral_centroid"],
        zero_crossing_rate=features["zero_crossing_rate"],
        rms_energy=features["rms_energy"],
        spectral_bandwidth=features["spectral_bandwidth"],
        chroma_mean=features["chroma_mean"]
    )

    db.add(audio_features)
    db.commit()
    db.refresh(audio_features)

    return {
        "song_id": song.id,
        "features_saved": True,
        "features": features
    }