import re

import requests
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager as DefaultUserManager
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models

from utils.fields import CustomImageField


class UserManager(DefaultUserManager):
    def get_or_create_facebook_user(self, user_info):
        username = '{}_{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            settings.FACEBOOK_APP_ID,
            user_info['id']
        )
        user, user_created = self.get_or_create(
            username=username,
            user_type=self.model.USER_TYPE_FACEBOOK,
            defaults={
                'last_name': user_info.get('last_name', ''),
                'first_name': user_info.get('first_name', ''),
                'email': user_info.get('email', ''),
            }
        )
        # 유저가 새로 생성되었을 때만 프로필 이미지를 받아옴
        if user_created and user_info.get('picture'):
            # 프로필 이미지 URL
            url_picture = user_info['picture']['data']['url']

            # 파일확장자를 가져와서 유저 고유의 파일명을 만들어줌
            p = re.compile(r'.*\.([^?]+)')
            file_ext = re.search(p, url_picture).group(1)
            file_name = '{}.{}'.format(
                user.pk,
                file_ext
            )

            # 이미지파일을 임시 저장할 파일 객체
            temp_file = NamedTemporaryFile()

            # 프로필 이미지 URL에 대한 get요청 (이미지 다운로드)
            response = requests.get(url_picture)

            # 요청 결과를 temp_file에 기록
            temp_file.write(response.content)

            # ImageField의 save()메서드를 호출해서 해당 임시파일객체를 주어진 이름의 파일로 저장
            # 저장하는 파일명은 위에서 만든 <유저pk.주어진 파일확장자>를 사용
            user.img_profile.save(file_name, File(temp_file))
        return user


class MyUser(AbstractUser):
    USER_TYPE_DJANGO = 'd'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_CHOICES = (
        (USER_TYPE_DJANGO, 'Django'),
        (USER_TYPE_FACEBOOK, 'Facebook'),
    )
    email = models.EmailField(null=True, unique=True)
    # 유저타입 기본은 Django 이며, Facebook 로그인 시 USER_TYPE_FACEBOOK값을 갖도록 함
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES, default=USER_TYPE_DJANGO)
    nickname = models.CharField(max_length=24, null=True, unique=True)
    img_profile = CustomImageField(
        upload_to='user',
        blank=True,
        default_static_image='images/profile.png',
    )

    # 위에서 만든 CustomUserManager를 objects속성으로 사용
    # User.objects.create_facebook_user()메서드
    objects = UserManager()

    def __str__(self):
        return self.nickname or self.username

