from django.conf.urls import url
from ..apis.reservations import ReservationListCreateView

urlpatterns = [
    url(r'^$', ReservationListCreateView.as_view())
]