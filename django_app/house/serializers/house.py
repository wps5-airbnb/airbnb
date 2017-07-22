from rest_framework import serializers

from member.serializers import UserSerializer
from ..models import House, Images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = '__all__'


class HouseSerializer(serializers.ModelSerializer):
    image = ImageSerializer(many=True, read_only=True)
    host = UserSerializer(read_only=True)

    class Meta:
        model = House
        fields = [
            'pk',
            'host',
            'title',
            'create_date',
            'modified_date',
            'address',
            'introduce',
            'space_info',
            'guest_access',
            'price_per_day',
            'extra_people_fee',
            'cleaning_fee',
            'weekly_discount',
            'accommodates',
            'bathrooms',
            'bedrooms',
            'beds',
            'room_type',
            'image',

        ]
        read_only_fields = [
            'pk',
            'create_date',
            'modified_date',
        ]
