
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^datasets/$', views.data_list, name='data_list'),
]