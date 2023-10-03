from django.urls import path
from .views import ActivityLogListCreateView

urlpatterns = [
    path('activity-logs/', ActivityLogListCreateView.as_view(), name='activity-logs-list-create'),
]
