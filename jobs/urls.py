from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<job_id>\d+)/$', views.detail, name='detail'),
    url(r'^create/', views.create, name='create'),
    url(r'^projects/', views.projects, name='projects'),
)