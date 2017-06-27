from django.shortcuts import render
from django.db.models import Q
from . import models


def books_by_genre(request, genre):
    books = models.Book.objects.filter(genre=genre)
    return render(request, 'products/bookGenreResult.html', {'books': books, 'genre': genre})


def get_book_by_author(request, author_id):
    author = models.Author.objects.filter(pk=author_id)
    books = models.Book.objects.filter(author_id=author_id)
    return render(request,'products/bookAuthorResult.html', {'books': books, 'author': author})


def get_book_details(request,title):
    book = models.Book.objects.get(title=title)
    book_by_author = models.Book.objects.filter(author_id=book.author.id)
    return render(request, 'products/bookDetail.html', {'book': book, 'book_by_author': book_by_author})


def search(request):
    search_request = request.GET.get('bookSearch')
    books = models.Book.objects.filter(
        Q(title__icontains=search_request) | Q(title__contains=search_request)
    )
    return render(request, 'products/bookSearchResult.html', {'books': books, 'search_request': search_request})


