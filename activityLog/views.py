from rest_framework import generics
from .models import ActivityLog
from .serializers import ActivityLogSerializer

class ActivityLogListCreateView(generics.ListCreateAPIView):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
