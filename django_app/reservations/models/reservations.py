from django.contrib.auth import get_user_model
from django.db import models
from house.models import House

User = get_user_model()


__all__ = [
    'Reservations',
    'Holiday',
]


class Reservations(models.Model):
    # 예약자
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
    )

    # 예약 인원
    adult_number = models.PositiveIntegerField(default=1)
    child_number = models.PositiveIntegerField(default=0)
    infant_number = models.PositiveIntegerField(default=0)

    # 체크인/체크아웃
    checkin_date = models.DateField(null=False, blank=False)
    checkout_date = models.DateField(null=False, blank=False)

    # 예약 날짜
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # 예약시 유저가 호스트에게 보내는 메세지
    message_to_host = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Name: {}\nCheck in: {} ~ Check out: {}'.format(
            self.user,
            self.checkin_date,
            self.checkout_date
        )


class Holiday(models.Model):
    # 임의로 예약 불가능 날짜를 정할 때
    name = models.CharField(max_length=100, blank=True)

    # 예약 불가능 날짜
    date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True, editable=True)

    # 설정시간
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}_{}'.format(self.name, self.date)
