from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^genre/(?P<genre>\w+)/$', views.books_by_genre, name='bookGenre'),
    url(r'^bookDetail/(?P<title>.*)/$', views.get_book_details, name='bookDetail'),
    url(r'^bookByAuthor/(?P<author_id>.*)/$', views.get_book_by_author, name='bookByAuthor'),
    url(r'search/$', views.search, name="search"),
]