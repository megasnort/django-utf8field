from rest_framework import serializers
from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('id', 'text', 'char', 'file', )
        extra_kwargs = {
            'file': {'max_content_length': 2000, 'four_byte_detection': True}
        }
