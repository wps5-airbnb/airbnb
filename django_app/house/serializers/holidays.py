from datetime import timedelta

from rest_framework import serializers

from ..models import House, Holidays


__all__ = [
    'HolidaySerializer',
]


class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holidays
        fields = [
            'pk',
            'name',
            'date',
            'active',
            'created_date',
            'updated_date',
        ]

        read_only_fields = [
            'pk',
            'created_date',
            'updated_date',
        ]

    def validate(self, data):
        date = data['date']

        house_pk = int(self.context["request"].query_params["house"])
        house = House.objects.get(pk=house_pk)
        current_user = self._context['request']._auth.user_id

        if house.host_id != current_user:
            raise serializers.ValidationError('Host 소유의 House만 등록 가능합니다')
        elif house.holidays_set.filter(date=date, active=True).exists():
            raise serializers.ValidationError('이미 휴일로 지정되어 있습니다')
        return data

    def save(self, *args, **kwargs):
        name = self.validated_data.get('name', '')
        house_pk = int(self.context["request"].query_params["house"])
        house = House.objects.get(pk=house_pk)
        date = self.validated_data.get('date', '')
        self.instance = Holidays.objects.create(
            name=name,
            house=house,
            date=date,
        )
        return self.instance


