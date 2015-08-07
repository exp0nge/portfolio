from django.conf.urls import url

from tracker import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/', views.add_series, name='add_series'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_series, name='delete_series'),
    url(r'^update/(?P<pk>[\w-]+)$', views.SeriesUpdate.as_view(), name='update_series'),
    url(r'^watched/(?P<pk>\d+)/$', views.update_episode, name='update_episode'),
    url(r'^watch_episode/(?P<pk>[\w-]+)$', views.watch_episode, name='watch_episode'),
    url(r'^stream_missing/(?P<pk>[\w-]+)$', views.stream_missing, name='stream_missing'),
    url(r'^favorite_site/$', views.add_favorite_site, name='add_favorite_site'),
    url(r'^get_favorite_sites/$', views.get_favorite_sites, name='get_favorite_sites'),
    url(r'^get_series_as_json/$', views.get_series_as_json, name='get_series_as_json'),
    url(r'^get_a_series/$', views.series_by_id_as_json, name='get_a_series_json'),
    url(r'^search/$', views.fuzzy_series_search, name='fuzzy_series_search'),
    url(r'^share_series/$', views.make_public, name='make_public'),
    url(r'^public_series_list/$', views.get_public_series_list, name='public_series_list'),
]
