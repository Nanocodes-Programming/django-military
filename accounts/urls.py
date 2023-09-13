from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (AwardsViewSet, CertificationViewSet, CustomUserViewSet,
                    EducationViewSet, InterestViewSet, LanguagesViewSet,
                    ProfileViewSet, WorkExperienceViewSet, UserViewSet, UserSearchView)

router = DefaultRouter()
# router.register(r'register', RegistrationView, basename='register')
router.register(r'profiles', ProfileViewSet, basename='profile')

router.register(r'users', CustomUserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'languages', LanguagesViewSet)
router.register(r'work-experiences', WorkExperienceViewSet)
router.register(r'awards', AwardsViewSet)
router.register(r'certifications', CertificationViewSet)
router.register(r'interests', InterestViewSet)
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('users/search/<str:keyword>', UserSearchView.as_view()),
]

