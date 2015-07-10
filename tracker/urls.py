from django.conf.urls import url

from tracker import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/', views.add_series, name='add_series'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_series, name='delete_series'),
    url(r'^update/(?P<pk>[\w-]+)$', views.SeriesUpdate.as_view(), name='update_series'),
    url(r'^watched/(?P<pk>\d+)/$', views.update_episode, name='update_episode'),
    url(r'^watch_episode/(?P<pk>[\w-]+)$', views.watch_episode, name='watch_episode'),

]
