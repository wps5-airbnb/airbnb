from django.db import models

__all__ = [
    'Reviews',
]


class Reviews(models.Model):
    visit_house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    writer = models.ForeignKey('member.MyUser', on_delete=models.CASCADE)
    contents = models.TextField(max_length=2000,)