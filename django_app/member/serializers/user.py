from rest_framework import serializers

from ..models import MyUser

__all__ = [
    'UserSerializer',
    'UserCreateSerializer',
]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = [
            'pk',
            'username',
            'email',
            'img_profile',
            'first_name',
            'last_name',
            'gender',
            'phone_num',
            'birthday',
            'preference_language',
            'preference_currency',
            'living_site',
            'introduce',
            'last_login',
            'date_joined',
        ]
        read_only_fields = [
            'pk',
            'username',
            'email',
            'last_login',
            'date_joined',
        ]


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    first_name = serializers.CharField(
        write_only=True,
        allow_blank=True,
        allow_null=True,
        default='null',
    )
    last_name = serializers.CharField(
        write_only=True,
        allow_blank=True,
        allow_null=True,
        default='null',
    )
    birthday = serializers.DateField(
        write_only=True,
        default='1990-01-01',
    )
    agreement = serializers.BooleanField(default=True)

    def validate_email(self, email):
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('This Email already exist')
        return email

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords didn\'t match')
        return data

    def validate_agreement(self, agreement):
        if not agreement:
            raise serializers.ValidationError("동의하지 않으면 가입이 안되요")
        return agreement

    def save(self, *args, **kwargs):
        email = self.validated_data.get('email', '')
        password = self.validated_data.get('password1', '')
        first_name = self.validated_data.get('first_name', '')
        last_name = self.validated_data.get('last_name', '')
        birthday = self.validated_data.get('birthday', '')
        user = MyUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
        )
        return user
