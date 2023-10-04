from rest_framework import serializers
from .models import ActivityLog
from accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","email","username","is_staff",]

class ActivityLogSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = ActivityLog
        fields = '__all__'
