from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class NewUserManager(UserManager):
    def create_facebook_user(self, user_info, username):
        return self.create_user(
            username=username,
            email=user_info.get('email', ''),
            first_name=user_info.get('first_name', ''),
            last_name=user_info.get('last_name', ''),
            user_type=MyUser.USER_TYPE_FACEBOOK
        )


class MyUser(AbstractUser):
    def __str__(self):
        return self.email

    USER_TYPE_DJANGO = 'django'
    USER_TYPE_FACEBOOK = 'facebook'
    CHOICES_USER_TYPE = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    user_type = models.CharField(max_length=20, choices=CHOICES_USER_TYPE, default=USER_TYPE_DJANGO)

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

    username = models.EmailField(unique=True)

    email = models.EmailField(unique=False)

    like_houses = models.ManyToManyField(
        'house.House',
        through='wishlist.Wishlist',
        related_name='wishlist_info'
    )

    objects = NewUserManager()
