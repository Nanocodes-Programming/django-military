from rest_framework import viewsets, permissions
from .models import IssueCategory, UserSupportIssue, SupportInfo
from .serializers import IssueCategorySerializer, UserSupportIssueSerializer
from accounts.views import IsStaffUserOrCreate, IsStaffUserOrReadOnly
class IssueCategoryViewSet(viewsets.ModelViewSet):
    queryset = IssueCategory.objects.all()
    serializer_class = IssueCategorySerializer
    permission_classes = [IsStaffUserOrReadOnly]

class UserSupportIssueViewSet(viewsets.ModelViewSet):
    queryset = UserSupportIssue.objects.all()
    serializer_class = UserSupportIssueSerializer
    permission_classes = [IsStaffUserOrCreate]

class SupportInfoViewSet(viewsets.ModelViewSet):
    queryset = SupportInfo.objects.all()
    serializer_class = UserSupportIssueSerializer
    permission_classes = [IsStaffUserOrReadOnly]