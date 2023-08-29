from rest_framework import viewsets, permissions
from .models import IssueCategory, UserSupportIssue, SupportInfo
from .serializers import IssueCategorySerializer, UserSupportIssueSerializer
from accounts.views import IsStaffUserOrReadOnly
class IssueCategoryViewSet(viewsets.ModelViewSet):
    queryset = IssueCategory.objects.all()
    serializer_class = IssueCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class UserSupportIssueViewSet(viewsets.ModelViewSet):
    queryset = UserSupportIssue.objects.all()
    serializer_class = UserSupportIssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupportInfoViewSet(viewsets.ModelViewSet):
    queryset = SupportInfo.objects.all()
    serializer_class = UserSupportIssueSerializer
    permission_classes = [IsStaffUserOrReadOnly]