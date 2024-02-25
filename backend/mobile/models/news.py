from typing import Optional
from uuid import uuid4
from django.db import models
import pendulum


from utils.web.fields import PendulumDateTimeField
from utils import SN, SNF
from cdn.utils import get_file_url
from cdn.models import FileStoreModel
from utils.web.field_handlers import rich_field_converter


class MobileNewsModel(models.Model):
    SN_public = SN(
        'uuid', 'created_at',
        name = SNF(str, limit=range(1, 100)),
        image = get_file_url(default = "/static/media_defaults/news.jpg"),
        content = rich_field_converter
    )
    
    class Meta:
        db_table = 'mobile_news'

    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    image: Optional[FileStoreModel] = models.OneToOneField(
        FileStoreModel, models.SET_NULL,
        null=True, related_name="news_images"
    )
    
    name: str = models.CharField(max_length=100, null=False)
    content: Optional[dict] = models.JSONField(null=True)
    
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)
