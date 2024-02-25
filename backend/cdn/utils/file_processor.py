from pathlib import Path
from typing import List, Optional, Tuple, Union
from django.core.files.uploadedfile import UploadedFile

from .const import FileType, FileStoreModel, BASE_PATH
from .process_file import process_file


class FormFileProcessor():
    
    def __init__(self) -> None:
        self._files: List[FileStoreModel] = []
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        if self._files:
            await self.utilize()
    
    async def process_file(
        self,
        file: UploadedFile,
        type: Union[List[FileType], FileType],
        dimensions: Optional[Union[int, Tuple[int, int]]] = None,
        max_size: Optional[int] = None,
    ) -> Optional[FileStoreModel]:
        file = await process_file(
            file=file,
            type=type,
            dimensions=dimensions,
            max_size=max_size,
            auto_create=False,
        )
        if file is not None:
            self._files.append(file)
        return file
    
    async def save(self):
        await FileStoreModel.objects.abulk_create(self._files)
        self._files.clear()
        
    async def utilize(self):
        for file in self._files:
            path: Path = (BASE_PATH / str(file.type) / file.uuid)
            path.unlink(missing_ok=True)
        self._files.clear()
    