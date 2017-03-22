from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^datasets/$', views.data_list, name='data_list'),
    url(r'^datasets/new/$', views.newData, name='newData'),
    url(r'^models/$', views.model_list, name='model_list'),
    url(r'^models/new/$', views.newModel, name='newModel'),
    url(r'^models/configure/$', views.modelConfig, name='modelConfig'),
    url(r'^reports/$', views.report_list, name='report_list'),
    url(r'^reports/new/$', views.newReport, name='newReport'),
    url(r'^reports/view', views.viewReport, name='viewReport'),
    url(r'^predict/$', views.predict, name='predict'),
]