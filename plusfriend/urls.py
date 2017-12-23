from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^keyboard$', views.on_init),
    url(r'^friend$', views.on_added),
    url(r'^friend/(?P<user_key>[\w-]+)$', views.on_block),
    url(r'^char_room/(?P<user_key>[\w-]+)$', views.on_leave),
    url(r'^message$', views.on_message),
    url(r'^diary/(?P<user_key>[a-zA-Z\d_-]+)$', views.post_list, name='post_list'),
]
