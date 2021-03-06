from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^create$', views.create),
    url(r'^secrets$', views.secrets),
    url(r'^logoff/?$', views.logoff),
    url(r'^secrets/post/?$', views.secret_post),
    url(r'^delete/(?P<id>\d+)/(?P<page>\w+)$', views.delete),
    url(r'^like/(?P<sID>\d+)/(?P<uID>\d+)/(?P<page>\w+)$', views.like),
    url(r'^secrets/$', views.popular),
]
