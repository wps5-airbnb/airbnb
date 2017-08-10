from django.contrib.auth import get_user_model
from django.db import models

__all__ = [
    'Reservations',
]

User = get_user_model()


class Reservations(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)

    checkin_date = models.DateField()
    checkout_date = models.DateField()

    available_dates = models.CharField(max_length=200, blank=True, null=True)
    disable_dates = models.CharField(max_length=200, blank=True, null=True)

    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)

    create_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
