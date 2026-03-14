from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.db import get_db
from backend.app.database.models import AudioFeatures, SongRating
from backend.app.services.song_rating import rate_song

router = APIRouter()


@router.post("/rate-song/{song_id}")
def rate_song_api(song_id: int, db: Session = Depends(get_db)):

    # Fetch audio features
    features = db.query(AudioFeatures).filter(AudioFeatures.song_id == song_id).first()

    if not features:
        raise HTTPException(status_code=404, detail="Audio features not found")

    feature_dict = {
        "tempo": features.tempo,
        "rms_energy": features.rms_energy,
        "spectral_centroid": features.spectral_centroid,
        "spectral_bandwidth": features.spectral_bandwidth,
        "chroma_mean": features.chroma_mean
    }

    rating = rate_song(feature_dict)

    # Store rating
    song_rating = SongRating(
        song_id=song_id,
        quality_score=rating["quality_score"],
        energy_score=rating["energy_score"],
        virality_score=rating["virality_score"],
        recommended_playlist=rating["recommended_playlist"]
    )

    db.add(song_rating)
    db.commit()

    return {
        "song_id": song_id,
        "rating": rating
    }