from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index , name = 'index'),
    url(r'^quote/$', views.quote , name = 'quote'),
    url(r'^result/$', views.result , name = 'result'),
    url(r'^buy/$', views.buy , name = 'buy'),
    url(r'^sell/$', views.sell , name = 'sell'),
]