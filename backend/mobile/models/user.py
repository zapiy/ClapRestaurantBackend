from typing import TYPE_CHECKING, Optional
from django.db import models
from uuid import uuid4
import pendulum

from utils.web.fields import PendulumDateTimeField, PendulumDateField
from utils import SN, SNF
from cdn.utils import get_file_url
from cdn.models import FileStoreModel
if TYPE_CHECKING:
    from .session import MobileSessionModel


class MobileUserModel(models.Model):
    SN_preview = SN(
        'uuid', 'full_name',
        avatar = get_file_url(default = "/static/media_defaults/avatar.jpg"),
    )
    
    SN_public = SN(
        'uuid', 'description',
        full_name = SNF(str, limit=range(1, 150)),
        email = SNF(str, limit=range(5, 120)),
        birthday = SNF(pendulum.Date.fromisoformat),
        working_at = SNF(pendulum.Date.fromisoformat),
        avatar = get_file_url(default = "/static/media_defaults/avatar.jpg"),
    )
    
    class Meta:
        db_table = 'mobile_user'
    
    class Status(models.TextChoices):
        NEWBIE = 'newbie'
        ACTIVE = 'active'
        LEAVE = 'leave'

    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    avatar: Optional[FileStoreModel] = models.OneToOneField(FileStoreModel, models.SET_NULL, null=True)
    
    full_name: str = models.CharField(max_length=150, null=False)
    
    email: str = models.EmailField(unique=True, null=False, max_length=120)
    description: Optional[str] = models.TextField(null=True, max_length=1000)

    status: Status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEWBIE,
    )

    password_hash: str = models.CharField(max_length=1000, null=False)

    birthday: pendulum.Date = PendulumDateField(null=False)
    working_at: pendulum.Date = PendulumDateField(auto_now_add=True)
    
    updated_at: pendulum.DateTime = PendulumDateTimeField(auto_now=True)
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)

    sessions: models.QuerySet['MobileSessionModel']
