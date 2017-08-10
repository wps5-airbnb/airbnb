from rest_framework import serializers

from ..models import Reservations

__all__ = [
    'ReservationSerializer',
]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservations
        fields = [
            'pk',
            'guest',
            'house',
            'checkin_date',
            'checkout_date',
            'available_dates',
            'disable_dates',
            'adults',
            'children',
            'create_date',
            'modified_date',
        ]
        read_only_fields = [
            'pk',
            'guest',
            'house',
            'create_date',
            'modified_date',
        ]
