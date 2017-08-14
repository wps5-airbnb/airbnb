from datetime import timedelta

from rest_framework import serializers

from house.models import House
from house.serializers.house import HouseSerializer
from member.models import MyUser
from member.serializers import UserSerializer
from ..models import Reservations, Holiday

__all__ = [
    'ReservationSerializer',
    'HolidaySerializer'
]


class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    house = HouseSerializer(read_only=True)

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
            'updated_date',
            'message_to_host',
            'house',
            'user',
        ]

        read_only_fields = [
            'pk',
            'created_date',
            'updated_date',
            'house',
            'user',
        ]

    def validate(self, data):
        checkin_date = data['checkin_date']
        checkout_date = data['checkout_date']
        dt = checkout_date - checkin_date

        house_pk = int(self.context["request"].query_params["house"])
        house = House.objects.get(pk=house_pk)

        reserved_date_list = [checkin_date + timedelta(n) for n in range(dt.days)]
        for date in reserved_date_list:
            if house.reservations_set.filter(checkin_date__lt=date, checkout_date__gt=date).exists():
                raise serializers.ValidationError('이미 예약되어있는 기간입니다.')
        return data

    # def validate_reserved_date(self, reserved_date):
    #     if Reservations.objects.filter(reserved_date=reserved_date).exists():
    #         raise serializers.ValidationError("Already reserved")
    #     return reserved_date

    # def validate_reserved_date(self, reserved_date):
    #     if Reservations.objects.filter(reserved_date=reserved_date).exists():
    #         raise serializers.ValidationError('Already reserved')
    #     return reserved_date

    def save(self, *args, **kwargs):
        user_pk = self.context["request"].auth.user.pk
        house_pk = int(self.context["request"].query_params["house"])
        user = MyUser.objects.get(pk=user_pk)
        house = House.objects.get(pk=house_pk)
        checkin_date = self.validated_data.get('checkin_date', '')
        checkout_date = self.validated_data.get('checkout_date', '')
        message_to_host = self.data["message_to_host"]
        Reservations.objects.create(
            user=user,
            house=house,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            # reserved_date=reserved_date,
            message_to_host=message_to_host,
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
