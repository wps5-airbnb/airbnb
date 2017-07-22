from rest_framework import serializers

from ..models import MyUser

__all__ = [
    'UserSerializer',
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'username',
        ]
