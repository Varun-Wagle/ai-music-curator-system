from fastapi import APIRouter, UploadFile, File, Form, Depends, BackgroundTasks
from sqlalchemy.orm import Session

from backend.app.database.db import get_db
from backend.app.database.models import Artist, Song
from backend.app.utils.file_handler import save_audio_file
from backend.app.services.audio_analysis import analyze_and_store

router = APIRouter()

@router.post("/submit-song")
async def submit_song(
    background_tasks: BackgroundTasks,
    artist_name: str = Form(...),
    email: str = Form(...),
    title: str = Form(...),
    genre: str = Form(...),
    mood: str = Form(...),
    audio: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Save audio file
    file_path = save_audio_file(audio, audio.filename)

    # Check if artist exists
    artist = db.query(Artist).filter(Artist.name == artist_name).first()

    if not artist:
        artist = Artist(name=artist_name, email=email)
        db.add(artist)
        db.commit()
        db.refresh(artist)

    # Create song
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

    # Extract integer ID
    song_id = song.id if hasattr(song, 'id') and isinstance(song.id, int) else int(getattr(song, 'id', 0))

    # Start background analysis
    background_tasks.add_task(analyze_and_store, song_id)

    return {
        "song_id": song_id,
        "artist": artist.name,
        "song": title,
        "stored_file": file_path
    }