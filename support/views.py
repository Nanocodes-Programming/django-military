from accounts.permissions import IsStaffUserOrCreate, IsStaffUserOrReadOnly
from activityLog.models import ActivityLog
from rest_framework import filters, viewsets

from .models import IssueCategory, SupportInfo, UserSupportIssue
from .serializers import IssueCategorySerializer, UserSupportIssueSerializer, SupportInfoSerializer


class IssueCategoryViewSet(viewsets.ModelViewSet):
    queryset = IssueCategory.objects.all()
    serializer_class = IssueCategorySerializer
    permission_classes = [IsStaffUserOrReadOnly]

class UserSupportIssueViewSet(viewsets.ModelViewSet):
    queryset = UserSupportIssue.objects.all()
    serializer_class = UserSupportIssueSerializer
    permission_classes = [IsStaffUserOrCreate]
    filter_backends = [filters.SearchFilter]

    def perform_create(self, serializer):
        activity_data = {
            'user': self.request.user,
            'action': 'Sent an issue',
        }
        ActivityLog.objects.create(**activity_data)
        serializer.save()


    def get_queryset(self):
        queryset = super().get_queryset()
        resolved = self.request.query_params.get('resolved', None)

        if resolved is not None:
            if resolved == 'true':
                queryset = queryset.filter(resolved=True)
            elif resolved == 'false':
                queryset = queryset.filter(resolved=False)
            else:
                queryset = queryset.none()

        return queryset

class SupportInfoViewSet(viewsets.ModelViewSet):
    queryset = SupportInfo.objects.all()
    serializer_class = SupportInfoSerializer
    permission_classes = [IsStaffUserOrReadOnly]
