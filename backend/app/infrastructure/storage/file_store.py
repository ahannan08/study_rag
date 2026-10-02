import uuid
from pathlib import Path

from app.config import get_settings


class FileStore:
    def __init__(self) -> None:
        self.settings = get_settings()

    def save_upload(self, user_id: uuid.UUID, document_id: uuid.UUID, filename: str, data: bytes) -> str:
        user_dir = self.settings.upload_dir / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(filename).suffix.lower() or ".bin"
        path = user_dir / f"{document_id}{ext}"
        path.write_bytes(data)
        return str(path)

    def delete_file(self, blob_path: str) -> None:
        p = Path(blob_path)
        if p.exists():
            p.unlink()
