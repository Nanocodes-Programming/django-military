from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'subject', 'read')
    list_filter = ('read',)
    search_fields = ('from_user', 'to_user__username', 'subject')
    ordering = ('-created_at',)

# Register your models with the admin site
admin.site.register(Message, MessageAdmin)
from django.contrib import admin

# Register your models here.
