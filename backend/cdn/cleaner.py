import asyncio, os

from .models import FileStoreModel
from .utils import BASE_PATH


async def cleaner():
    BASE_PATH.mkdir(exist_ok=True)
    while True:
        for model in FileStoreModel.objects.filter(recycle = True).all():
            os.remove(str(BASE_PATH / model.uuid))
            await model.adelete()
        await asyncio.sleep(1800)
