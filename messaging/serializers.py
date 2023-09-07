from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    from_user = serializers.UUIDField(read_only=True)
    class Meta:
        model = Message
        fields = '__all__'
