from django.conf.urls import url

from ..apis import HouseCreateListView

urlpatterns = [
    url(r'^$', HouseCreateListView.as_view()),
]
