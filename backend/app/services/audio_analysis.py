import librosa
import numpy as np
from sqlalchemy.orm import Session
from backend.app.database.models import AudioFeatures, Song
from backend.app.database.db import SessionLocal


def analyze_audio(file_path: str):
    """
    Analyze an audio file and extract musical features.
    """

    # Load audio
    y, sr = librosa.load(file_path)

    # Duration
    duration = librosa.get_duration(y=y, sr=sr)

    # Tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    tempo = float(np.atleast_1d(tempo)[0])

    # Spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = float(np.mean(spectral_centroid))

    # Zero crossing rate
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    zcr_mean = float(np.mean(zero_crossing_rate))

    # RMS energy (loudness intensity)
    rms = librosa.feature.rms(y=y)
    rms_mean = float(np.mean(rms))

    # Spectral bandwidth (spread of frequencies)
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    spectral_bandwidth_mean = float(np.mean(spectral_bandwidth))

    # Chroma features (harmonic structure)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    chroma_mean = float(np.mean(chroma))

    return {
        "tempo": tempo,
        "duration": float(duration),
        "spectral_centroid": spectral_centroid_mean,
        "zero_crossing_rate": zcr_mean,
        "rms_energy": rms_mean,
        "spectral_bandwidth": spectral_bandwidth_mean,
        "chroma_mean": chroma_mean
    }

def analyze_and_store(song_id: int):

    db = SessionLocal()

    try:
        song = db.query(Song).filter(Song.id == song_id).first()

        if not song:
            return {"error": "Song not found"}

        file_path = str(song.file_path)

        features = analyze_audio(file_path)

        audio_features = AudioFeatures(
            song_id=song_id,
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

    finally:
        db.close()