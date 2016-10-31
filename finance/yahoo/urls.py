from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index , name = 'index'),
    url(r'^quote/$', views.quote , name = 'quote'),
    url(r'^result/$', views.result , name = 'result'),
    url(r'^buy/$', views.buy , name = 'buy'),
    url(r'^sell/$', views.sell , name = 'sell'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^history/$', views.history, name='history'),
    url(r'^error/$', views.error, name='error'),
]