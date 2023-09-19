from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueCategoryViewSet, UserSupportIssueViewSet, SupportInfoViewSet

router = DefaultRouter()
router.register(r'issue-categories', IssueCategoryViewSet)
router.register(r'user-support-issues', UserSupportIssueViewSet)
router.register(r'support', SupportInfoViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
