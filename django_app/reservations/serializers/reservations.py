from datetime import timedelta

from rest_framework import serializers

from house.models import House, DisableDay
from house.serializers.house import HouseSerializer
from member.models import MyUser
from member.serializers import UserSerializer
from ..models import Reservations

__all__ = [
    'ReservationSerializer',
]


class ReservationSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    house = HouseSerializer(read_only=True)

    class Meta:
        model = Reservations
        fields = [
            'pk',
            'adults',
            'children',
            'infants',
            'checkin_date',
            'checkout_date',
            'created_date',
            'updated_date',
            'message_to_host',
            'house',
            'guest',
        ]

        read_only_fields = [
            'pk',
            'created_date',
            'updated_date',
            'house',
            'guest',
        ]

    def validate(self, data):
        checkin_date = data['checkin_date']
        checkout_date = data['checkout_date']

        schedule_of_stay = checkout_date - checkin_date

        house_pk = int(self.context["request"].query_params["house"])
        house = House.objects.get(pk=house_pk)

        reserved_date_list = [checkin_date + timedelta(n) for n in range(schedule_of_stay.days)]
        disable_date_list = [i.date for i in house.disable_days.all()]
        print('{}'.format(disable_date_list))
        for day in reserved_date_list:
            if day in disable_date_list:
                raise serializers.ValidationError('예약 불가능한 날짜입니다.')

        return data

    def save(self, *args, **kwargs):
        guest_pk = self.context["request"].auth.user.pk
        house_pk = int(self.context["request"].query_params["house"])
        guest = MyUser.objects.get(pk=guest_pk)
        house = House.objects.get(pk=house_pk)
        checkin_date = self.validated_data.get('checkin_date', '')
        checkout_date = self.validated_data.get('checkout_date', '')
        message_to_host = self.validated_data.get('message_to_host', '')
        Reservations.objects.create(
            guest=guest,
            house=house,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            message_to_host=message_to_host,
        )
        reserved_date_list = [checkin_date + timedelta(n) for n in range((checkout_date-checkin_date).days)]
        for date in reserved_date_list:
            date_instance, created = DisableDay.objects.get_or_create(date=date)
            house.disable_days.create(
                date=date_instance.date,
            )


