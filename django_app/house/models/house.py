from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

__all__ = [
    'House',
    'Images',
]


User = get_user_model()


class House(models.Model):
    title = models.TextField(max_length=100)
    host = models.ForeignKey(User, )
    address = models.TextField(max_length=200)
    introduce = models.TextField(max_length=500)
    space_info = models.TextField(max_length=500)
    guest_access = models.TextField(max_length=300)

    # price
    price_per_day = models.PositiveIntegerField()
    extra_people_fee = models.PositiveIntegerField()
    cleaning_fee = models.PositiveIntegerField()
    weekly_discount = models.IntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )

    #space
    ROOM_TYPE_CHOICE = (
        ('House', '집전체'),
        ('Individual', '개인실'),
        ('Shared_Room', '다인실')
    )
    accommodates = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    beds = models.PositiveIntegerField()
    room_type = models.CharField(
        max_length=20,
        choices=ROOM_TYPE_CHOICE,
        default='House',
    )


class Images(models.Model):
    house = models.ForeignKey(House, related_name='image')
    image = models.ImageField(
        upload_to='HouseImage',
        blank=True,
        null=True,
    )
