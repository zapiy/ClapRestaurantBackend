from typing import Callable, Optional
from django.conf import settings

from ..models import FileStoreModel


def get_file_url(default: Optional[str] = None) -> Callable[[FileStoreModel], str]:
    return lambda model: settings.INTERNET_URL + (
        (default if default else None)
        if model is None else 
        f'/cdn/{model.type}/{model.uuid}'
    )
    