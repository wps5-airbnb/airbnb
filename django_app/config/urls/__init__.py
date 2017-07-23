from django.conf.urls import url, include

from . import urls_views

urlpatterns = [
    url(r'^', include(urls_views)),
]