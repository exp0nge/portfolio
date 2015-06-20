from django.conf.urls import url

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'project-list/', views.project_list, name='project_list'),
    url(r'project/(?P<project_title_slug>[\w\-]+)/$', views.project, name='project')
]
