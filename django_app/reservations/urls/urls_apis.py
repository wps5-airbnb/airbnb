from django.conf.urls import url
from .. import apis

urlpatterns = [
    url(r'^$', apis.ReservationCreateListView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.ReservationRetrieveUpdateDestroyView.as_view()),
]

