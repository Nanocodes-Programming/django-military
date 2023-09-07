import random
import string

from accounts.models import CustomUser
from accounts.permissions import IsStaff
from common.responses import CustomErrorResponse, CustomSuccessResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from utils.communications.email import send_reset_request_mail
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import ChangePasswordSerializer, ResetPasswordSerializer


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

                send_reset_request_mail(user_data, password)
                return CustomSuccessResponse(message='Password reset successful.')
            else:
                return CustomErrorResponse(message='No user found.', status=status.HTTP_404_NOT_FOUND)
    
        else:
            return CustomErrorResponse(data=serializer.errors)

