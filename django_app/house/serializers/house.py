from rest_framework import serializers

from member.serializers import UserSerializer
from reservations.serializers import ReservationSerializer
from ..models import House, Images, Amenities


class AmenitieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = [
            'name',
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = [
            '_order',
            'image',
        ]


class HouseSerializer(serializers.ModelSerializer):
    house_images = ImageSerializer(many=True, read_only=True, source='image')
    amenities = AmenitieSerializer(many=True, read_only=True, )
    host = UserSerializer(read_only=True)
    reservations = ReservationSerializer(source='reservations_set', many=True)
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
            'house_images',
            'amenities',
            'latitude',
            'longitude',
            'reservation_user_set',
        ]
        read_only_fields = [
            'pk',
            'create_date',
            'modified_date',
            'amenities',
            'reservation_user_set',
        ]


class HouseUpdateSerializer(HouseSerializer):
    image_crusher = serializers.CharField(
        write_only=True,
        allow_blank=True,
        allow_null=True,
        default='null',
    )

    class Meta(HouseSerializer.Meta):
        fields = HouseSerializer.Meta.fields + ["image_crusher"]
