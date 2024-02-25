from django.db import models
from django.conf import settings
from utils import generate_token
from datetime import datetime

from utils.web.fields import PendulumDateTimeField
from utils import SN


def get_new_uuid() -> str:
    while True:
        token = generate_token(40) + "_" + generate_token(110)
        if not FileStoreModel.objects.filter(uuid=token).exists():
            return token


class FileStoreModel(models.Model):
    SN_public = SN(
        "uuid", "type",
        url = lambda model: settings.INTERNET_URL + f"/cdn/{model.type}/{model.uuid}"
    )
    
    class Meta:
        db_table = 'file_store'
        
    class Type(models.TextChoices):
        FILE = "file"
        IMAGE = "image"
        VIDEO = "video"

    uuid: str = models.CharField(primary_key=True, editable=False, max_length=200, default=get_new_uuid)
    name: str = models.CharField(max_length=200, null=True)
    type: Type = models.CharField(
        max_length=20,
        choices=Type.choices,
        null=False
    )
    
    recycle: bool = models.BooleanField(default=False)
    checked_at: datetime = models.DateTimeField(auto_now=True)
