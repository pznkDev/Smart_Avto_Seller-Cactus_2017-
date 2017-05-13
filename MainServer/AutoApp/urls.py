from django.conf.urls import url

from AutoApp import views

urlpatterns = [
    url(r'load$', views.load)
]
