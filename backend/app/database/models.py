from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from backend.app.database.db import Base


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