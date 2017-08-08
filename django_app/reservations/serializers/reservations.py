from rest_framework import serializers

from house.serializers.house import HouseSerializer
from member.serializers import UserSerializer
from ..models import Reservations, Holiday


__all__ = [
    'ReservationSerializer',
    'HolidaySerializer'
]


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    house = HouseSerializer(read_only=True, many=True)

    class Meta:
        model = Reservations
        fields = [
            'pk',
            'adult_number',
            'child_number',
            'infant_number',
            'checkin_date',
            'checkout_date',
        ]

        read_only_fields = [
            'pk',
            'username',
            'email',
            'house',
            'created_date',
            'updated_date'
        ]


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