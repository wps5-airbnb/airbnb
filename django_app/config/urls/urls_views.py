from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from .. import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^member/', include('member.urls.url_views')),
    url(r'^$', views.Index.as_view(), name='index'),
]
# /static/에 대한 요청을 STATIC_ROOT경로의 파일에서 찾는다
urlpatterns += static(prefix=settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# /media/에 대한 요청을 MEDIA_ROOT경로의 파일에서 찾는다
urlpatterns += static(prefix=settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
