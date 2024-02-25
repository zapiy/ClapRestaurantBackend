from enum import Enum
from typing import Awaitable, Callable, Dict, Optional
from django.http import HttpRequest
from django.db.models import Model
from urllib.parse import urlparse
import orjson

from cdn.utils import FormFileProcessor, FileType
from utils import SN, SNF


class FieldType(Enum):
    IMAGE = 'image'
    RICH = 'rich'

SUPPORTED_QUILL_BLOB_TYPES = ["image", "video"]
RICH_FIELD_DEFINION = SNF(orjson.loads, validate=lambda x: isinstance(x, list))

def _check_required(model: Model, field_name: str):
    field = next(filter(lambda f: f.name == field_name, model._meta.fields), None)
    if not field:
        return False
    is_required = not field.null
    if is_required and getattr(model, field_name) is None:
        return True
    return False


async def handle_post_fields(
    request: HttpRequest, 
    model: Model,
    *,
    mapping: Optional[SN] = None,
    extra: Dict[str, FieldType] = None,
    side_processing: Callable[[HttpRequest, Model], Awaitable[bool]] = None,
):
    assert (mapping or extra)
    
    if mapping is not None:
        data = mapping.parse(request.POST, model)
        if not data:
            return True
    
    if (
        side_processing is not None 
        and (await side_processing(request, model))
    ):
        return True
    
    if extra is not None:
        async with FormFileProcessor() as files:
            for key, type in extra.items():
                if type == FieldType.IMAGE:
                    if key in request.FILES:
                        image = await files.process_file(
                            request.FILES[key], FileType.IMAGE,
                        )
                        if not image:
                            return True
                        setattr(model, key, image)
                    elif _check_required(model, key):
                        return True
                elif type == FieldType.RICH:
                    if key in request.POST:
                        content = SN.safe_get(request.POST, key, RICH_FIELD_DEFINION)
                        if content is None:
                            return True
                        
                        attachments = {}
                        if "attachments" in request.FILES:
                            for file in request.FILES.getlist('attachments'):
                                attachments[file.name] = file
                        
                        parsed_content = []
                        for line in content:
                            if "insert" not in line: continue
                            if isinstance(line['insert'], str):
                                parsed_content.append(line)
                            elif isinstance(line['insert'], dict):
                                blob_key = next(filter(lambda k: k in line['insert'], SUPPORTED_QUILL_BLOB_TYPES), None)
                                if not blob_key: continue
                                blob_url: str = line['insert'][blob_key]
                                if not len(blob_url) > 15: continue
                                
                                if blob_url.startswith('blob:'):
                                    blob_uuid = urlparse(blob_url[5:]).path[1:]
                                    if (
                                        len(blob_uuid) not in range(30, 50)
                                        or blob_uuid not in attachments
                                    ):
                                        return True
                                    
                                    attach = await files.process_file(
                                        attachments[blob_uuid], {
                                            "image": FileType.IMAGE,
                                            "video": FileType.VIDEO,
                                        }.get(blob_key, FileType.FILE))
                                    
                                    if attach is None:
                                        return True
                                    
                                    line['insert'] = { blob_key: f"/cdn/{attach.type}/{attach.uuid}" }
                                    parsed_content.append(line)
                                    
                                elif blob_url.startswith('http') and '/cdn/' in blob_url:
                                    blob_uuid = urlparse(blob_url[5:]).path
                                    line['insert'] = { blob_key: blob_uuid }
                                    parsed_content.append(line)
                        
                        setattr(model, key, content)
                    elif _check_required(model, key):
                        return True
                        
            await files.save()
            
    return False
