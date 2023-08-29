from rest_framework import serializers
from .models import IssueCategory, UserSupportIssue, SupportInfo

class IssueCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueCategory
        fields = '__all__'

class UserSupportIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSupportIssue
        fields = '__all__'

class SupportInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportInfo
        fields = '__all__'