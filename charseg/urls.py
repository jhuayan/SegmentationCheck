from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<pk>[0-9A-Za-z-]*)$', views.run_seg),
    url(r'^run_cut/(?P<pk>[0-9A-Za-z-]*)$', views.run_cut),
]
