from typing import Optional
from uuid import uuid4
from django.db import models

from utils import SN, SNF
from utils.web.field_handlers import rich_field_converter
from cdn.utils import get_file_url
from cdn.models import FileStoreModel


class MobileFoodCategoryModel(models.Model):
    SN_public = SN(
        'uuid',
        name = SNF(str, limit=range(1, 100)),
        image = get_file_url(default = "/static/media_defaults/food.jpg"),
        has_foods = lambda o: o.foods.count() > 0,
        children = "children_"
    )
    
    class Meta:
        db_table = 'mobile_food_category'

    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    image: Optional[FileStoreModel] = models.OneToOneField(FileStoreModel, models.SET_NULL, null=True)
    
    name: str = models.CharField(max_length=100, null=False)
    parent: Optional['MobileFoodCategoryModel'] = models.ForeignKey(
        'self', models.SET_NULL, 
        null=True, related_name="children",
        db_constraint=False
    )
    children: models.QuerySet['MobileFoodCategoryModel']
    foods: models.QuerySet['MobileFoodModel']
    
    @property
    def children_(self):
        return list(MobileFoodCategoryModel.objects.filter(parent = self).all())
    

class MobileFoodModel(models.Model):
    SN_public = SN(
        'uuid', 
        name = SNF(str, limit=range(1, 100)),
        image = get_file_url(default = "/static/media_defaults/food.jpg"),
        content = rich_field_converter
    )
    
    class Meta:
        db_table = 'mobile_food'

    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    image: Optional[FileStoreModel] = models.OneToOneField(FileStoreModel, models.SET_NULL, null=True)
    
    name: str = models.CharField(max_length=100, null=False)
    category: MobileFoodCategoryModel = models.ForeignKey(
        MobileFoodCategoryModel, models.CASCADE,
        null=False, related_name="foods"
    )
    content: Optional[dict] = models.JSONField(null=True)
