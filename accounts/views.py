from authentication.views import randomPassword
from activityLog.models import ActivityLog
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.communications.email import send_signup_mail
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .models import (Award, Certification, CustomUser, Education, Interest,
                     Language, Profile, WorkExperience)
from .permissions import IsStaffUserOrReadOnly, ProfilePermissions
from .serializers import (AwardsSerializer, CertificationSerializer,
                          CustomUserSerializer, EducationSerializer,
                          InterestSerializer, LanguagesSerializer,
                          ProfileSerializer,
                          WorkExperienceSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsStaffUserOrReadOnly]

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create(self, request, *args, **kwargs):
        profile_data = request.data.pop('profile', None)
        
        # Create the CustomUser instance without the profile data
        request_data = request.data
        request_data.pop('password', None)
        password = randomPassword()
        hashed_password = make_password(password)
        request_data['password'] = hashed_password
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)

        # Call the modified perform_create method
        user = self.perform_create(serializer)

        # Check if profile data was provided
        if profile_data:
            # Create the Profile instance and link it to the CustomUser
            profile_data.update({"user": user.id})
            profile_serializer = ProfileSerializer(data=profile_data)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
        user_data = {
            "email": user.email,
            "username": user.username,
            "phone_number": user.phone_number,
        }
        activity_data = {
                'user':user,
                'action' : 'Viewed users',
                }

        ActivityLog.objects.create(**activity_data)

        user_data.update({"password":password})
        send_signup_mail(user_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [ProfilePermissions]

    def get_queryset(self):
        return Profile.objects.select_related(
            'user',
            ).prefetch_related(
                'educations',
                'languages',
                'work_experiences',
                'awards',
                'certifications',
                'interests'
            )

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class LanguagesViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguagesSerializer
    permission_classes = [IsStaffUserOrReadOnly]
    def get_object(self):
        profile_id = self.kwargs.get('pk')
        obj = get_object_or_404(Language, profile=profile_id)
        return obj

class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class AwardsViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardsSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)

class UserSearchView(APIView):
    def get(self, request, *args, **kwargs):

        # Get the search keyword from the URL parameter
        keyword = kwargs['keyword']

        # Filter users based on email and/or name
        users = CustomUser.objects.all()

        if keyword:
            # Use Q objects to perform OR queries on multiple fields
            users = users.filter(
                Q(email__icontains=keyword) |
                Q(profile__first_name__icontains=keyword) |
                Q(profile__last_name__icontains=keyword)
            )

        # Serialize the filtered users
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
