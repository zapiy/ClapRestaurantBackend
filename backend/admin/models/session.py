from typing import Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from enum import Enum
import pendulum

from utils import generate_token
from utils.web.fields import PendulumDateTimeField
from .admin import AdminUserModel


def get_new_session_key() -> str:
    while True:
        token = generate_token(32) + "_" + generate_token(64)
        if not AdminSessionModel.objects.filter(session_key=token).exists():
            return token


class AdminPermission(Enum):
    OWNER = 5
    ADMIN = 1


class AdminSessionModel(models.Model):
    class Meta:
        db_table = 'admin_session'
    
    session_key = models.CharField(_('session key'), max_length=100, primary_key=True, default=get_new_session_key)
    csrf_token: str = models.CharField(_('csrf token'), max_length=16, null=True)

    user: Optional[AdminUserModel] = models.ForeignKey(
        AdminUserModel, related_name="sessions", 
        on_delete=models.CASCADE, null=True,
    )

    updated_at: pendulum.DateTime = PendulumDateTimeField(auto_now=True)
    created_at: pendulum.DateTime = PendulumDateTimeField(auto_now_add=True)
    
    def update_csrf_token(self):
        self.csrf_token = generate_token(16)
    
    @property
    def permission_level(self):
        return (
            AdminPermission.OWNER.value
            if self.user is None else
            AdminPermission.ADMIN.value
        )
    
    def has_permission(self, permission: AdminPermission):
        return (self.permission_level >= permission.value)
