from fastapi import APIRouter, UploadFile, File, Form
from backend.app.utils.file_handler import save_audio_file

router = APIRouter()


@router.post("/submit-song")
async def submit_song(
    artist_name: str = Form(...),
    email: str = Form(...),
    title: str = Form(...),
    genre: str = Form(...),
    mood: str = Form(...),
    audio: UploadFile = File(...)
):

    file_path = save_audio_file(audio, audio.filename)

    return {
        "artist": artist_name,
        "song": title,
        "stored_file": file_path
    }