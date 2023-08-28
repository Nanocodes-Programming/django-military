from django.contrib import admin
from .models import IssueCategory, UserSupportIssue, SupportInfo

class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)

class UserSupportIssueAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'issue_category', 'resolved')
    list_filter = ('resolved', 'issue_category')
    search_fields = ('user__username', 'issue_category__title')
    ordering = ('-created_at',)

class SupportInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'address')

# Register your models with the admin site
admin.site.register(IssueCategory, IssueCategoryAdmin)
admin.site.register(UserSupportIssue, UserSupportIssueAdmin)
admin.site.register(SupportInfo, SupportInfoAdmin)
