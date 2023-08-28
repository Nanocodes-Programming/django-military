from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from .choices import GENDER_CHOICES
from common.models import BaseModel
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)        
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=20)
    is_suspended = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    def __str__(self):
        return self.username


class Profile(BaseModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    personal_number = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    commisson = models.CharField(max_length=100 ,null=True,blank=True)
    unit = models.CharField(max_length=100)
    role = models.CharField(max_length=255)
    crop = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True,blank=True)
    state_of_origin = models.CharField(max_length=50 ,null=True,blank=True)
    lga = models.CharField(max_length=50 ,null=True,blank=True)
    blood_group = models.CharField(max_length=255 ,null=True,blank=True)
    blood_genotype = models.CharField(max_length=255 ,null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    bio = models.TextField(null=True ,null=True,blank=True)
    image = models.ImageField(upload_to='', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user} {self.first_name} {self.last_name}" 


class Education(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    school = models.CharField(max_length=250)
    type_of = models.CharField(max_length=250)
    certification = models.CharField(max_length=225)
    date_from = models.DateField()
    date_to = models.DateField()
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.profile

class Languages(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    language = models.CharField(max_length=250)

    def __str__(self):
        return self.profile

class WorkExperience(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    name = models.CharField(max_length=250)
    position = models.CharField(max_length=250)
    description = models.TextField(null=True,blank=True)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return self.profile

class Awards(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    name = models.CharField(max_length=250)
    date_given = models.DateField()
    description = models.TextField( null=True,blank=True)   
    def __str__(self):
        return self.profile

class Certification(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    name = models.CharField(max_length=250)
    organisation = models.CharField(max_length=250)
    date_given = models.DateField()
    description = models.TextField( null=True,blank=True)
    def __str__(self):
        return self.profile

class Interest(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.profile


class Ranks(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    date_given = models.DateField()
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.profile
