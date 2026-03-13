import os
from backend.app.core.config import UPLOAD_DIR


def save_audio_file(file, filename):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(UPLOAD_DIR, filename)

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path