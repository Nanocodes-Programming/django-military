from django.db import models
from common.models import BaseModel
from accounts.models import CustomUser

User = CustomUser
# Create your models here.
class Message(BaseModel):
    from_user = models.CharField
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,)
    subject = models.CharField(max_length=250)
    body = models.TextField()
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.subject} to {self.to_user}"
