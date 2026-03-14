from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.sql import func
from backend.app.database.db import Base
from sqlalchemy import Float

class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    spotify_link = Column(String)
    country = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    title = Column(String)
    genre = Column(String)
    mood = Column(String)
    file_path = Column(String)
    status = Column(String, default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AudioFeatures(Base):
    __tablename__ = "audio_features"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("songs.id"))

    tempo = Column(Float)
    duration = Column(Float)
    spectral_centroid = Column(Float)
    zero_crossing_rate = Column(Float)

    rms_energy = Column(Float)
    spectral_bandwidth = Column(Float)
    chroma_mean = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SongRating(Base):
    __tablename__ = "song_ratings"

    id = Column(Integer, primary_key=True, index=True)
    song_id = Column(Integer, ForeignKey("songs.id"))

    quality_score = Column(Float)
    energy_score = Column(Float)
    virality_score = Column(Float)

    recommended_playlist = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

