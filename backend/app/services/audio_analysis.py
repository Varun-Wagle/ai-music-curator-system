import librosa
import numpy as np


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
    tempo = float(np.atleast_1d(tempo)[0])  # Ensure it's a float, not an array

    # Spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = float(np.mean(spectral_centroid))

    # Zero crossing rate
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    zcr_mean = float(np.mean(zero_crossing_rate))

    return {
        "tempo": float(tempo),
        "duration": float(duration),
        "spectral_centroid": spectral_centroid_mean,
        "zero_crossing_rate": zcr_mean
    }