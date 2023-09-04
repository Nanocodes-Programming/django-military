from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseModel
# Create your models here.
User = get_user_model()

class IssueCategory(BaseModel):
    title = models.CharField(max_length=255)

    def __str__(self):
        return str(self.title)

class UserSupportIssue(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_category = models.ForeignKey(IssueCategory, on_delete=models.CASCADE)
    body = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.issue_category)

class SupportInfo(BaseModel):
    email = models.EmailField(null=True,blank=True)
    email2 = models.EmailField(null=True,blank=True)
    email3 = models.EmailField(null=True,blank=True)
    phone = models.CharField(max_length=300,null=True,blank=True)
    phone2 = models.CharField(max_length=300,null=True,blank=True)
    phone3 = models.CharField(max_length=300,null=True,blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    address2 = models.CharField(max_length=300,null=True,blank=True)
    address3 = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return str(self.email)