from django.conf.urls import url, include


urlpatterns = [
    url(r'^house/', include('house.urls.urls_apis')),
    url(r'^user/', include('member.urls.urls_apis')),
    url(r'^reservations/', include('reservations.urls.urls_apis')),
    url(r'^like/', include('wishlist.urls.urls_apis')),
]
