from rest_framework import viewsets, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import (Awards, Certification, CustomUser, Education, Interest,
                     Languages, Profile, Ranks, WorkExperience)
from .serializers import (AwardsSerializer, CertificationSerializer,
                          CustomUserSerializer, EducationSerializer,
                          InterestSerializer, LanguagesSerializer,
                          ProfileSerializer, RanksSerializer,
                          WorkExperienceSerializer)


class UserLoginView(TokenObtainPairView):
    pass

class IsStaffUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsStaffUserOrCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_staff

class ProfilePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [ProfilePermissions]

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class LanguagesViewSet(viewsets.ModelViewSet):
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsStaffUserOrReadOnly]

class AwardsViewSet(viewsets.ModelViewSet):
    queryset = Awards.objects.all()
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

class RanksViewSet(viewsets.ModelViewSet):
    queryset = Ranks.objects.all()
    serializer_class = RanksSerializer
    permission_classes = [IsStaffUserOrReadOnly]
