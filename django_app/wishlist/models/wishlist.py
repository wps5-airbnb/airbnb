from django.db import models


# Create your models here.

class Wishlist(models.Model):
    likers = models.ForeignKey('member.MyUser', on_delete=models.CASCADE)
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
