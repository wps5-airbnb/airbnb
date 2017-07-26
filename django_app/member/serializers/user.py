from rest_framework import serializers

from ..models import MyUser

__all__ = (
    'UserSerializer',
    'UserUpdateSerializer',
    'UserCreationSerializer',
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'pk',
            'username',
            'email',
            'nickname',
            'img_profile',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = (
            'pk',
            'username',
            'ori_password',
            'password1',
            'password2',
            'img_profile',
        )
        read_only_fields = (
            'username',
            'email',
        )


class UserCreationSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=100,
    )
    password1 = serializers.CharField()
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exist')
        return username

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords didn\'t match')
        return data

    def save(self, *args, **kwargs):
        username = self.validated_data.get('username', '')
        password = self.validated_data.get('password1', '')
        user = User.objects.create_user(
            username=username,
            password=password
        )
        return user
