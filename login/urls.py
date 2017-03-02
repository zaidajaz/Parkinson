
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^login_auth/$', views.login_auth, name="login_auth"),
    url(r'^logout/$', views.logout, name="logout"),
]
