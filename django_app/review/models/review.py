from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

__all__ = [
    'Review',
    'Rating',
]


class Review(models.Model):
    author = models.ForeignKey('member.MyUser', on_delete=models.CASCADE)
    house = models.ForeignKey('house.House', on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    rating = models.OneToOneField('Rating')


class Rating(models.Model):
    accuracy = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    location = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    communication = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    checkin = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    cleanliness = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
    value = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(5),
        ]
    )
