from rest_framework import serializers
from .models import CustomUser, Profile, Education, Language, WorkExperience, Award, Certification, Interest, Rank
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

class AwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = '__all__'

class RanksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rank
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    languages = LanguagesSerializer(many=True, read_only=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    awards = AwardsSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    interests = InterestSerializer(many=True, read_only=True)
    ranks = RanksSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'created_at', 'updated_at', 'personal_number', 'first_name', 'last_name', 'middle_name', 'commisson', 'unit', 'role', 'crop', 'date_of_birth', 'state_of_origin', 'lga', 'blood_group', 'blood_genotype', 'gender', 'bio', 'image', 'user', 'educations','languages','work_experiences','awards','certifications','interests','ranks', ]


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ["id","created_at","email","username","phone_number","is_suspended","password","is_staff","profile",]

    def validate_password(self, value):
        # Validate password using Django's built-in password validators
        try:
            validate_password(value, self.instance)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        return user
