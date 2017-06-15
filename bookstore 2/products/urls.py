from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^genre/(?P<genre>\w+)/$', views.booksByGenre, name='bookGenre'),
    url(r'search/$', views.search, name="search"),
]