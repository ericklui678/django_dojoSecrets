from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^create$', views.create),
    url(r'^secrets$', views.secrets),
    url(r'^logoff/?$', views.logoff),
    url(r'^secrets/post/?$', views.secret_post),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^pdelete/(?P<id>\d+)$', views.delete),
    url(r'^like/(?P<sID>\d+)/(?P<uID>\d+)$', views.like),
    url(r'^plike/(?P<sID>\d+)/(?P<uID>\d+)$', views.plike),
    url(r'^secrets/$', views.popular),
]
