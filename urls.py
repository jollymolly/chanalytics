from django.conf.urls import url

from .views import DefaultView, SearchView
from .apps import ChanalyticsConfig

app_name = ChanalyticsConfig.name

urlpatterns = [
    url(r'^$', DefaultView(), name='default'),
    url(r'^search/$', SearchView(), name='search'),
]
