from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueCategoryViewSet, UserSupportIssueViewSet

router = DefaultRouter()
router.register(r'issue-categories', IssueCategoryViewSet)
router.register(r'user-support-issues', UserSupportIssueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
