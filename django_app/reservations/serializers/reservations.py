from rest_framework import serializers

from house.models import House
from member.models import MyUser
from ..models import Reservations, Holiday


__all__ = [
    'ReservationSerializer',
    'HolidaySerializer'
]


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservations
        fields = [
            'pk',
            'adult_number',
            'child_number',
            'infant_number',
            'checkin_date',
            'checkout_date',
            'created_date',
            'updated_date'
        ]

        read_only_fields = [
            'pk',
            'created_date',
            'updated_date'
        ]

    def save(self, **kwargs):
        user_pk = self.context["request"].auth.user.pk
        house_pk = int(self.context["request"].parser_context["kwargs"]['pk'])
        user = MyUser.objects.get(pk=user_pk)
        house = House.objects.get(pk=house_pk)
        checkin_date = self.validated_data["checkin_date"]
        checkout_date = self.validated_data["checkout_date"]
        Reservations.objects.create(
            user=user,
            house=house,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
        )


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = [
            'name',
            'date',
            'active',
        ]

        read_only_fields = [
            'created_date',
            'updated_date'
        ]
