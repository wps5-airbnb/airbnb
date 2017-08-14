from django.conf.urls import url
from rest_framework.authtoken import views

from .. import apis

urlpatterns = [
    url(r'^$', apis.UserCreateListView.as_view()),
    url(r'^login/$', apis.obtain_auth_token),
    url(r'^logout/$', apis.UserLogoutView.as_view()),
    url(r'^(?P<pk>\d+)/$', apis.UserRetrieveUpdateDestroyView.as_view()),
    url(r'^facebook-login/$', apis.FacebookLoginView.as_view()),
]