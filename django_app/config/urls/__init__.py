from django.conf.urls import url, include

from . import urls_views, urls_apis

urlpatterns = [
    url(r'^', include(urls_views)),
    url(r'^api/', include(urls_apis)),
]