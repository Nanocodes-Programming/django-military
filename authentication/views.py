from accounts.models import CustomUser
from accounts.permissions import IsStaff
from common.responses import CustomErrorResponse, CustomSuccessResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import ChangePasswordSerializer, ResetPasswordSerializer


class UserLoginView(TokenObtainPairView):
    pass

class Logout(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, token):
        token = RefreshToken(token)
        token.blacklist()
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
            user = CustomUser.objects.get(id=serializer.validated_data['id'])
            if user:
                user.set_password(serializer.validated_data['password'])
                user.save()
                return CustomSuccessResponse(message='Password reset successful.')
            else:
                return CustomErrorResponse(message='No user found.', status=status.HTTP_404_NOT_FOUND)
    
        else:
            return CustomErrorResponse(data=serializer.errors)

