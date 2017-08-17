from django.db import models

__all__ = [
    'Wishlist',
]


class Wishlist(models.Model):
    def __str__(self):
        return '{}의 pk={}하우스 좋아요'.format(self.liker.username, self.house.pk)

    liker = models.ForeignKey('member.MyUser', on_delete=models.CASCADE)
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
