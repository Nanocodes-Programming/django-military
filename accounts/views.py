from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, status
from .serializers import UserSerializer, ProfileSerializer
from .models import CustomUser, Profile
from django.shortcuts import get_object_or_404


class UserLoginView(TokenObtainPairView):
    pass

class RegistrationView(viewsets.ViewSet):
    def create(self, request):
        custom_user_serializer = UserSerializer(data=request.data)

        if custom_user_serializer.is_valid(raise_exception=True):
            user = custom_user_serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User registered successfully!",
                    "data": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response({'error': 'Invalid data'}, status=status.HTTP_400_BAD_REQUEST)
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        user_id = self.kwargs.get('pk')
        obj = get_object_or_404(Profile, user=user_id)
        return obj

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer