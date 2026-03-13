from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from backend.app.database.db import get_db
from backend.app.database.models import Artist, Song
from backend.app.utils.file_handler import save_audio_file

router = APIRouter()

@router.post("/submit-song")
async def submit_song(
    artist_name: str = Form(...),
    email: str = Form(...),
    title: str = Form(...),
    genre: str = Form(...),
    mood: str = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Save the uploaded audio file
    file_path = save_audio_file(audio, audio.filename)

    # Check if artist already exists, if not create a new one
    artist = db.query(Artist).filter(Artist.name == artist_name).first()
    if not artist:
        artist = Artist(name=artist_name, email=email)
        db.add(artist)
        db.commit()
        db.refresh(artist)

    # Create a new song entry
    song = Song(
        artist_id=artist.id,
        title=title,
        genre=genre,
        mood=mood,
        file_path=file_path
    )
    db.add(song)
    db.commit()
    db.refresh(song)

    return {
        "song_id": song.id,
        "artist": artist.name,
        "song": title,
        "stored_file": file_path
    }