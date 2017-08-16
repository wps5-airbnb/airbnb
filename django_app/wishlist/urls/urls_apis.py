from django.conf.urls import url
from ..apis.wishlist import WishlistView

urlpatterns = [
    url(r'^$', WishlistView.as_view()),
]