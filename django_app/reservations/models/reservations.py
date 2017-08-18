from django.contrib.auth import get_user_model
from django.db import models

from house.models import House

User = get_user_model()

__all__ = [
    'Reservations',
]


class Reservations(models.Model):
    # 예약자
    guest = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
    )

    # 예약 인원
    adults = models.PositiveIntegerField(default=1, blank=False)
    children = models.PositiveIntegerField(default=0)
    infants = models.PositiveIntegerField(default=0)

    # 체크인/체크아웃
    checkin_date = models.DateField(null=False, blank=False)
    checkout_date = models.DateField(null=False, blank=False)

    # 예약 날짜
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # 예약시 유저가 호스트에게 보내는 메세지
    message_to_host = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}님\nCheck in: {} ~ Check out: {} 일자의 예약'.format(
            self.guest,
            self.checkin_date,
            self.checkout_date
        )

