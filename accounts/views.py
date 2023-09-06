from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import (Award, Certification, CustomUser, Education, Interest,
                     Language, Profile, Rank, WorkExperience)
from .permissions import IsStaffUserOrReadOnly, ProfilePermissions
from .serializers import (AwardsSerializer, CertificationSerializer,
                          CustomUserSerializer, EducationSerializer,
                          InterestSerializer, LanguagesSerializer,
                          ProfileSerializer, RanksSerializer,
                          WorkExperienceSerializer)


from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, ProfileSerializer, AwardsSerializer, LanguagesSerializer, WorkExperienceSerializer, EducationSerializer, CertificationSerializer, InterestSerializer, RanksSerializer
from common.responses import CustomErrorResponse, CustomSuccessResponse
from authentication.views import randomPassword
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsStaffUserOrReadOnly]

    def perform_create(self, serializer):
        user = serializer.save()
        return user

    def create(self, request, *args, **kwargs):
        profile_data = request.data.pop('profile', None)
        education_data = request.data.pop('educations', None)
        language_data = request.data.pop('languages', None)
        work_experience_data = request.data.pop('work-experiences', None)
        award_data = request.data.pop('awards', None)
        certification_data = request.data.pop('certifications', None)
        interest_data = request.data.pop('interests', None)
        rank_data = request.data.pop('ranks', None)
        
        # Create the CustomUser instance without the profile data
        request_data = request.data
        request_data.pop('password', None)
        password = randomPassword()
        request_data.update({'password': password})
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
            profile_serializer.save(user=user)

        # Check if award data was provided and create it similarly
        if award_data:
            award_data.update({"profile": profile_serializer.instance.id})
            award_serializer = AwardsSerializer(data=award_data)
            award_serializer.is_valid(raise_exception=True)
            award_serializer.save()

        # Check if language data was provided and create it similarly
        if language_data:
            for data in language_data:
                data.update({"profile": profile_serializer.instance.id})
                language_serializer = LanguagesSerializer(data=data)
                language_serializer.is_valid(raise_exception=True)
                language_serializer.save()

        # Check if work_experience data was provided and create it similarly
        if work_experience_data:
            for data in work_experience_data:
                data.update({"profile": profile_serializer.instance.id})
                work_experience_serializer = WorkExperienceSerializer(data=data)
                work_experience_serializer.is_valid(raise_exception=True)
                work_experience_serializer.save()

        # Check if education data was provided and create it similarly
        if education_data:
            for data in education_data:
                data.update({"profile": profile_serializer.instance.id})
                education_serializer = EducationSerializer(data=data)
                education_serializer.is_valid(raise_exception=True)
                education_serializer.save()

        # Check if certification data was provided and create it similarly
        if certification_data:
            for data in certification_data:
                data.update({"profile": profile_serializer.instance.id})
                certification_serializer = CertificationSerializer(data=data)
                certification_serializer.is_valid(raise_exception=True)
                certification_serializer.save()

        # Check if interest data was provided and create it similarly
        if interest_data:
            for data in interest_data:
                data.update({"profile": profile_serializer.instance.id})
                interest_serializer = InterestSerializer(data=data)
                interest_serializer.is_valid(raise_exception=True)
                interest_serializer.save()

        # Check if rank data was provided and create it similarly
        if rank_data:
            for data in rank_data:
                data.update({"profile": profile_serializer.instance.id})
                rank_serializer = RanksSerializer(data=data)
                rank_serializer.is_valid(raise_exception=True)
                rank_serializer.save()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [ProfilePermissions]

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsStaffUserOrReadOnly]
    def get_object(self):
        profile_id = self.kwargs.get('pk')
        obj = get_object_or_404(Education, profile=profile_id)
        return obj

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
    def get_object(self):
        profile_id = self.kwargs.get('pk')
        obj = get_object_or_404(WorkExperience, profile=profile_id)
        return obj

class AwardsViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardsSerializer
    permission_classes = [IsStaffUserOrReadOnly]
    def get_object(self):
        profile_id = self.kwargs.get('pk')
        obj = get_object_or_404(Award, profile=profile_id)
        return obj

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    permission_classes = [IsStaffUserOrReadOnly]
    def get_object(self):
        profile_id = self.kwargs.get('pk')
        obj = get_object_or_404(Certification, profile=profile_id)
        return obj

class InterestViewSet(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer
    permission_classes = [IsStaffUserOrReadOnly]
    def get_object(self):
        profile_id = self.kwargs.get('pk')
        obj = get_object_or_404(Interest, profile=profile_id)
        return obj

class RanksViewSet(viewsets.ModelViewSet):
    queryset = Rank.objects.all()
    serializer_class = RanksSerializer
    permission_classes = [IsStaffUserOrReadOnly]
    def get_object(self):
        profile_id = self.kwargs.get('pk')
        obj = get_object_or_404(Rank, profile=profile_id)
        return obj
