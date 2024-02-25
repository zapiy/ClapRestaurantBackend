from django.conf import settings
from ..models import FileStoreModel


FileType = FileStoreModel.Type
EXTENSION_TABLE = {
    FileType.IMAGE: ["jpg", "jpeg", "png"],
    FileType.VIDEO: ["avi", "mp3", "mp4"],
}

BASE_PATH = settings.BASE_DIR / "stored"
