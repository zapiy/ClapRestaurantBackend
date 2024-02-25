from typing import Optional

from ..models import FileStoreModel


async def ensure_recycle(model: Optional[FileStoreModel]):
    if isinstance(model, FileStoreModel):
        model.recycle = True
        await model.asave(force_update=True)
