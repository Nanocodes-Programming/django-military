from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (AwardsViewSet, CertificationViewSet, CustomUserViewSet,
                    EducationViewSet, InterestViewSet, LanguagesViewSet,
                    ProfileViewSet, RanksViewSet, 
                    UserLoginView, WorkExperienceViewSet)

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
router.register(r'ranks', RanksViewSet)

urlpatterns = [
    path('', include(router.urls)),
]



urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'),
]
