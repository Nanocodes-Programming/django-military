from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Education, Language, WorkExperience, Award, Certification, Interest

class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'phone_number', 'is_active', 'is_staff', 'is_suspended')
    list_filter = ('is_active', 'is_staff', 'is_suspended')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'phone_number', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_suspended', 'user_permissions')}),
    )

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'unit', 'gender')
    list_filter = ('unit', 'gender')
    search_fields = ('user__username', 'first_name', 'last_name', 'unit')
    ordering = ('user__username',)

class EducationAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'school', 'date_from', 'date_to')
    list_filter = ('school',)
    search_fields = ('profile__user__username', 'school')
    ordering = ('profile__user__username',)

class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'language')

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'name', 'position', 'date_from', 'date_to')

class AwardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'name', 'date_given')

class CertificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'name', 'organisation', 'date_given')

class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'name')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Language, LanguagesAdmin)
admin.site.register(WorkExperience, WorkExperienceAdmin)
admin.site.register(Award, AwardsAdmin)
admin.site.register(Certification, CertificationAdmin)
admin.site.register(Interest, InterestAdmin)
