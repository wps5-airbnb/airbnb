from uuid import uuid4

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


def f():
    """
    랜덤한 코드를 생성해주는 함수
    :return: 헤시된 랜덤 값을 리턴
    """
    d = uuid4()
    str = d.hex
    return str[0:16]


class NewUserManager(BaseUserManager):
    """
    username을 없애고 email을 기준으로 오버라이드 시킴
    """

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class MyUser(AbstractUser):
    def __str__(self):
        return self.email

    GENDER_CHOICE = (
        ('MALE', '남자'),
        ('FEMALE', '여자'),
        ('OTHER', '기타'),
    )
    img_profile = models.ImageField(upload_to='user', blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICE,
        default='OTHER',
    )
    birthday = models.DateField(blank=True, null=True)
    phone_num = models.CharField(max_length=20, blank=True, null=True)
    preference_language = models.CharField(max_length=20, blank=True, null=True)
    preference_currency = models.CharField(max_length=20, blank=True, null=True)
    living_site = models.CharField(max_length=100, blank=True, null=True)
    introduce = models.TextField(max_length=300, blank=True, null=True)

    username = models.EmailField()
    identifier = models.CharField(max_length=40, unique=True, default=f)  # createsuperuser 할때만 적용
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['identifier', ]

    like_houses = models.ManyToManyField(
        'house.House',
        through='wishlist.Wishlist',
        related_name='wishlist_info'
    )

    objects = NewUserManager()
