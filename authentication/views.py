import random
import string

from accounts.models import CustomUser
from accounts.permissions import IsStaff
from activityLog.models import ActivityLog
from common.responses import CustomErrorResponse, CustomSuccessResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import serializers, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from utils.communications.email import send_reset_request_mail

from .serializers import ChangePasswordSerializer, ResetPasswordSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema

User = CustomUser

def randomPassword():
    characters = string.ascii_letters + string.digits + "*.$#,"
    random_string = ''.join(random.choice(characters) for _ in range(10))
    return random_string

class UserLoginView(TokenObtainPairView):
    pass

class Logout(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, token):
        try: 
            token = RefreshToken(token)
            token.blacklist()
            return CustomSuccessResponse(message="successfully logged out")
        except TokenError:
            return CustomSuccessResponse(message="successfully logged out")


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            # Check if the old password matches the user's current password
            if not user.check_password(serializer.validated_data['old_password']):
                return CustomErrorResponse(message='Old password is incorrect.')
            
            user.set_password(serializer.validated_data['new_password'])
            user.save()

                    #add to log
            activity_data = {
            'user':user,
            'action' : 'Changed password',
            }

            ActivityLog.objects.create(**activity_data)

            return CustomSuccessResponse(message='Password changed successfully.')
        else:
            return CustomErrorResponse(data=serializer.errors)
 

class ResetPassword(APIView):
    permission_classes = [IsStaff]

    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.get(id=serializer.validated_data['user_id'])
            if user:
                password = randomPassword()
                user.set_password(password)
                user.save()

                user_data = {
                "id": user.id,
                "created_at": user.created_at,
                "email": user.email,
                "username": user.username,
                "phone_number": user.phone_number,
                "is_suspended": user.is_suspended,
                "is_staff": user.is_staff,
                # Include other fields you want here
            }
                activity_data = {
                'user':user,
                'action' : 'Password was reset',
                }

                ActivityLog.objects.create(**activity_data)
                
                send_reset_request_mail(user_data, password)
                return CustomSuccessResponse(message='Password reset successful.')
            else:
                return CustomErrorResponse(message='No user found.', status=status.HTTP_404_NOT_FOUND)
    
        else:
            return CustomErrorResponse(data=serializer.errors)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer  # Use a single class, not a list

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        username = validated_data.get('username')
        password = validated_data.get('password')
        
        user, token = self.login_user(username, password)
        user_data = {
                "id": user.id,
                "created_at": user.created_at,
                "email": user.email,
                "username": user.username,
                "phone_number": user.phone_number,
                "is_suspended": user.is_suspended,
                "is_staff": user.is_staff,
                # Include other fields you want here
            }
        data = {
            "access": token.get("access"),
            "refresh": token.get("refresh"),
            "user": user_data  # Use the serializer directly here
        }
        #add to log
        activity_data = {
        'user':user,
        'action' : 'Logged in',
        }

        ActivityLog.objects.create(**activity_data)
        return Response(data=data, status=status.HTTP_200_OK)

    def login_user(self, username, password):
        # Check if the user exists and is active
        try:
            user = User.objects.get(username=username)
            if not user.is_active:
                raise serializers.ValidationError(
                    {"username": ["This user is currently not active. Kindly verify your email."]}
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"username": ["Invalid login details."]}
            )

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                {"username": ["Invalid login details."]}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"username": ["This user is currently not active. Kindly contact support."]}
            )

        # Generate and return the tokens
        token = self.get_token_for_user(user)
        return user, token

    def get_token_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        last_login = timezone.now() + timezone.timedelta(hours=1)
        user.last_login = last_login
        user.save()

        refresh['email'] = user.email

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
