from typing import TYPE_CHECKING
from django.db import models
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from utils import SN, SNF
from utils.web.fields import PendulumDateTimeField
import pendulum

from utils import generate_token
if TYPE_CHECKING:
    from .session import AdminSessionModel


def get_new_auth_token() -> str:
    while True:
        token = generate_token(32) + "_" + generate_token(64)
        if not AdminUserModel.objects.filter(auth_token=token).exists():
            return token


class AdminUserModel(models.Model):
    SN_public = SN(
        'uuid', "auth_token", "created_at",
        key_name = SNF(str, limit=range(1, 50)),
    )
    
    class Meta:
        db_table = 'admin_user'
    
    uuid: str = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    key_name: str = models.CharField(_('key name'), max_length=50, null=False)
    auth_token = models.CharField(_('auth token'), max_length=100, null=False, db_index=True, default=get_new_auth_token)

    sessions: models.QuerySet['AdminSessionModel']
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)
    