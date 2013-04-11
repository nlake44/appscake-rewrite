from django.conf.urls import url, patterns


urlpatterns = patterns('appscake.views',
                       url(r'^$', 'home', name='home'),
                       url(r'^$', 'about', name='about'),
                       )
