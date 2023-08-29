from django.db import models
from common.models import BaseModel
from accounts.models import CustomUser

class Message(BaseModel):
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    from_name = models.CharField(max_length=255, blank=True, null=True)
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=250)
    body = models.TextField()
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.from_user} to {self.to_user}: {self.subject}"
