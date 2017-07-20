from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    def __init__(self):
        return self.username

    img_profile = models.ImageField(upload_to='user', blank=True)
