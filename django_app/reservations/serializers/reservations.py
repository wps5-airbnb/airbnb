from rest_framework import serializers, filters

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
    checkin_date = filters.django_filters.DateFilter(name='date', lookup_expr='gte')
    checkout_date = filters.django_filters.DateFilter(name='date', lookup_expr='lte')
    # reserved_date = filters.django_filters.DateRangeFilter(name='date')
    class Meta:
        model = Reservations
        fields = [
            'pk',
            'adult_number',
            'child_number',
            'infant_number',
            'checkin_date',
            'checkout_date',
            # 'reserved_date',
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

    def validate_checkin_date(self, checkin_date):
        if Reservations.objects.filter(checkin_date=checkin_date).exists():
            raise serializers.ValidationError('Already reserved')
        return checkin_date

    def validate_checkout_date(self, checkout_date):
        if Reservations.objects.filter(checkout_date=checkout_date).exists():
            raise serializers.ValidationError('Already reserved')
        return checkout_date

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
        # reserved_date = self.validated_data.get('reserved_date', '')
        Reservations.objects.create(
            user=user,
            house=house,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            message_to_host=message_to_host,
            # reserved_date=reserved_date,
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
