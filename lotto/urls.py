from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^lotto/$', views.index, name='lotto'),
    url(r'^$', views.index, name='index'),
    url(r'^lotto/new/$', views.post, name = "new_lotto"),
    url(r'^lotto/crawling/$', views.crawling, name = "new_data"),
    url(r'^lotto/(?P<lottokey>[0-9]+)/detail/$', views.detail, name='detail'),
]
