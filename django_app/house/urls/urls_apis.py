from django.conf.urls import url

from ..apis import HouseCreateListView, HouseRetrieveUpdateDestroyView, HouseCreateListViewWithPage, \
    HolidaysCreateListView, HolidaysRetrieveUpdateDestroyView

urlpatterns = [
    url(r'^$', HouseCreateListView.as_view()),
    url(r'^(?P<pk>\d+)/$', HouseRetrieveUpdateDestroyView.as_view()),
    url(r'^separated/$', HouseCreateListViewWithPage.as_view()),
    url(r'^holidays/$', HolidaysCreateListView.as_view()),
    url(r'^holidays/(?P<pk>\d+)/$', HolidaysRetrieveUpdateDestroyView.as_view()),
]
