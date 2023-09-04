from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ChangePassword, Logout, ResetPassword, UserLoginView

urlpatterns = [
    path('auth/login/', UserLoginView.as_view(), name='user-login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'),
    path('auth/logout/', Logout.as_view()),
    path('auth/change-password/', ChangePassword.as_view()),
    path('auth/reset-password/', ResetPassword.as_view()),
    
]
