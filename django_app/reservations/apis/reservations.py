from rest_framework import generics

from ..models import Reservations
from ..serializer import ReservationSerializer

__all__ = [
    'ReservationListCreateView'
]


class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservations.objects.all()
    serializer_class = ReservationSerializer
