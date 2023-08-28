from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserLoginView, RegistrationView, ProfileViewSet, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'register', RegistrationView, basename='register')
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'),
]
