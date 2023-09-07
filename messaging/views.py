import uuid

from accounts.models import CustomUser
from common.responses import CustomErrorResponse, CustomSuccessResponse
from rest_framework import filters, permissions, status, viewsets

from .models import Message
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        queryset = super().get_queryset()
        read = self.request.query_params.get('read', None)

        if read is not None:
            if read == 'true':
                queryset = queryset.filter(read=True)
            elif read == 'false':
                queryset = queryset.filter(read=False)
            else:
                queryset = queryset.none()

        return queryset

    def create(self, request, *args, **kwargs):
        # Get the value of the 'to_user' field from the request data
        to_user_value = request.data.get('to_user', None)
        
        # Check if 'to_user' is 'all'
        if to_user_value == 'all':
            # Send the message to all users in the database
            to_users = CustomUser.objects.all()
        elif isinstance(to_user_value, list):
            to_users = CustomUser.objects.filter(id__in=to_user_value)
            pass
        else:
            # Check if 'to_user' is a UUID (user ID)
            try:
                to_user_uuid = uuid.UUID(to_user_value)
                to_users = [CustomUser.objects.get(id=to_user_uuid)]
            except (ValueError, CustomUser.DoesNotExist):
                # If it's not a UUID or user doesn't exist, treat it as an empty list
                to_users = []
        
        # Create a message for each recipient
        for to_user in to_users:
            message_data = {
                'from_user': request.user.id,
                'to_user': to_user.id,
                'subject': request.data.get('subject', ''),
                'body': request.data.get('body', ''),
                'from_name': request.data.get('from_name', '')
            }
            message_serializer = MessageSerializer(data=message_data)
            if message_serializer.is_valid():
                message_serializer.save()
            else:
                return CustomErrorResponse(data=message_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return CustomSuccessResponse(message='Messages sent successfully.', status=status.HTTP_201_CREATED)
