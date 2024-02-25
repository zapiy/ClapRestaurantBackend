from typing import List, Optional, Tuple, Union
from django.core.files.uploadedfile import UploadedFile
from shutil import copyfileobj
from pathlib import Path

from cdn.models import FileStoreModel, get_new_uuid
from .const import FileType, EXTENSION_TABLE, BASE_PATH
from .. import processors


async def process_file(
    file: UploadedFile,
    type: Union[List[FileType], FileType],
    dimensions: Optional[Union[int, Tuple[int, int]]] = None,
    max_size: Optional[int] = None,
    auto_create: bool = True,
):
    if max_size is not None and (
        file.size is None
        or file.size <= 0
        or file.size > max_size
    ):
        return None
    
    if isinstance(type, list):
        if not file.name: return None
        ext = file.name.rpartition(".")[2]
        ext_type = next((t for t, ex in EXTENSION_TABLE.items() if ext in ex), FileType.FILE)
        if ext_type not in type:
            return None
        type = ext_type
    
    uuid = get_new_uuid()
    path: Path = (BASE_PATH / str(type))
    path.mkdir(parents=True, exist_ok=True)
    path = str(path / uuid)
    
    if type == FileType.IMAGE:
        try:
            processors.process_image(
                stream=file.file,
                file_path=path,
                max_dimention=(dimensions or 500)
            )
        except:
            return None
    
    else:
        with open(path, 'wb') as f:
            copyfileobj(file.file, f)
    
    name = None
    if file.name:
        name = file.name
        
        if type != FileType.FILE:
            name = name.partition(".")[0]
        
        if len(name) > 200:
            name = name[:80] + "__" + name[-80:]
    
    kwargs = {
        'uuid': uuid,
        'name': name,
        'type': type
    }
    
    if auto_create:
        return await FileStoreModel.objects.acreate(**kwargs)
    return FileStoreModel(**kwargs)
