from django.conf.urls import url

from ..apis import HouseCreateListView, HouseRetrieveUpdateDestroyView

urlpatterns = [
    url(r'^$', HouseCreateListView.as_view()),
    url(r'^(?P<pk>\d+)/$', HouseRetrieveUpdateDestroyView.as_view()),
]
