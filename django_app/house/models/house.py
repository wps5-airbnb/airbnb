from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

__all__ = [
    'House',
    'Images',
    'Amenities',
]

User = get_user_model()


class House(models.Model):
    def __str__(self):
        return self.title

    # general
    title = models.TextField(max_length=300)
    host = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    address = models.TextField(max_length=200, blank=True, null=True)
    introduce = models.TextField(max_length=1000, blank=True, null=True)
    space_info = models.TextField(max_length=1000, blank=True, null=True)
    guest_access = models.TextField(max_length=1000, blank=True, null=True)

    # price
    price_per_day = models.PositiveIntegerField()
    extra_people_fee = models.PositiveIntegerField()
    cleaning_fee = models.PositiveIntegerField()
    weekly_discount = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )

    # space
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
    amenities = models.ManyToManyField(
        'Amenities',
        related_name='amenities_manager',
    )

    latitude = models.FloatField(verbose_name='위도')
    longitude = models.FloatField(verbose_name='경도')


class Images(models.Model):
    def __str__(self):
        return "image_{}_{}".format(self.house.pk, self.pk)

    house = models.ForeignKey(
        House,
        related_name='image',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='HouseImage',
        blank=True,
        null=True,
    )

    class Meta:
        order_with_respect_to = 'house'


class Amenities(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
