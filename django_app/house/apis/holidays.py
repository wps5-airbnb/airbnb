from rest_framework import generics, permissions, filters

from utils.permissions import IsHouseOwner, ObjectIsRequestUser, IsHolidayHouseOwner
from ..serializers import HolidaySerializer
from ..models import Holidays

__all__ = [
    'HolidaysCreateListView',
    'HolidaysRetrieveUpdateDestroyView',
]


class HolidaysCreateListView(generics.ListCreateAPIView):
    queryset = Holidays.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('house',)

    def perform_create(self, serializer):
        serializer.save()


class HolidaysRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Holidays.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsHolidayHouseOwner,
    ]
