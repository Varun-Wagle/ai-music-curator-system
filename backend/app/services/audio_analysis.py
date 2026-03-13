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