from rest_framework import serializers
from .models import CustomUser, Profile, Education, Languages, WorkExperience, Awards, Certification, Interest, Ranks
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class LanguagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Languages
        fields = '__all__'

class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'

class AwardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Awards
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
        model = Ranks
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
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate_password(self, value):
        # Validate password using Django's built-in password validators
        try:
            validate_password(value, self.instance)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        educations_data = profile_data.pop('educations', [])
        languages_data = profile_data.pop('languages', [])
        work_experiences_data = profile_data.pop('work_experiences', [])
        awards_data = profile_data.pop('awards', [])
        certifications_data = profile_data.pop('certifications', [])
        interests_data = profile_data.pop('interests', [])
        ranks_data = profile_data.pop('ranks', [])

        user = CustomUser.objects.create(**validated_data)
        profile = Profile.objects.create(user=user, **profile_data)

        for education_data in educations_data:
            Education.objects.create(profile=profile, **education_data)
        for language_data in languages_data:
            Languages.objects.create(profile=profile, **language_data)
        for work_experience_data in work_experiences_data:
            WorkExperience.objects.create(profile=profile, **work_experience_data)
        for award_data in awards_data:
            Awards.objects.create(profile=profile, **award_data)
        for certification_data in certifications_data:
            Certification.objects.create(profile=profile, **certification_data)
        for interest_data in interests_data:
            Interest.objects.create(profile=profile, **interest_data)
        for rank_data in ranks_data:
            Ranks.objects.create(profile=profile, **rank_data)

        return user
