from django.conf.urls import *
from appscake import views


urlpatterns = patterns('appscake.views',
    url(r'^$', 'home', name='home'),
    (r'^about/$', 'about',),
    (r'^common/.*', 'common',),
    url(r'virtualbox/$', views.virtualbox_form),
    url(r'start/$', 'start'),

    )



