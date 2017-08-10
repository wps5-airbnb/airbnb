from django.conf.urls import url, include

from ..apis import HouseCreateListView, HouseRetrieveUpdateDestroyView, HouseCreateListViewWithPage

urlpatterns = [
    url(r'^$', HouseCreateListView.as_view()),
    url(r'^(?P<house_pk>\d+)/$', HouseRetrieveUpdateDestroyView.as_view()),
    url(r'^separated/$', HouseCreateListViewWithPage.as_view()),
    url(r'^(?P<house_pk>\d+)/reservations/', include('reservations.urls.urls_apis')),
]
