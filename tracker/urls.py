from django.conf.urls import url

from tracker import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/', views.add_series, name='add_series'),
    url(r'^delete/(?P<pk>\d+)/$', views.delete_series, name='delete_series'),

]
