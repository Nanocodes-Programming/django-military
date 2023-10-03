from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseModel
User = get_user_model()

class ActivityLog(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created_at}"
