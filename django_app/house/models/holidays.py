from django.db import models

from ..models import House

__all__ = [
    'Holidays',
]


class Holidays(models.Model):
    # Holiday 등록 숙소
    house = models.ForeignKey(
        House,
        on_delete=models.CASCADE,
    )

    # 임의로 예약 불가능 날짜를 정할 때
    name = models.CharField(max_length=100, blank=False)

    # 예약 불가능 날짜
    date = models.DateField(null=False, blank=False)
    active = models.BooleanField(default=True, editable=True)

    # 설정시간
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}_{}'.format(self.name, self.date)
