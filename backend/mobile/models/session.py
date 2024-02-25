from typing import Optional
from django.db import models
import pendulum

from utils.web.fields import PendulumDateTimeField
from utils import generate_token
from .user import MobileUserModel


def get_new_auth_token() -> str:
    while True:
        token = generate_token(32) + "_" + generate_token(64)
        if not MobileSessionModel.objects.filter(auth_token=token).exists():
            return token


class MobileSessionModel(models.Model):
    class Meta:
        db_table = 'mobile_session'
    
    class Status(models.TextChoices):
        ACTIVE = 'active'
        EXPIRED = 'expired'
    
    auth_token: str = models.CharField(primary_key=True, db_index=True, max_length=120, default=get_new_auth_token)
    fcm_token: str = models.CharField(max_length=255, null=False)
    
    user: Optional[MobileUserModel] = models.ForeignKey(
        MobileUserModel, related_name="sessions", 
        on_delete=models.CASCADE, null=True,
    )
    
    status: Status = models.CharField(
        max_length=15,
        choices=Status.choices,
    )
    
    extra: dict = models.JSONField(null=True)
    
    updated_at: pendulum.DateTime = PendulumDateTimeField(auto_now=True)
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)
