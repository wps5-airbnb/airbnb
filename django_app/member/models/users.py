from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
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
