from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from . import models
from django.views.generic import CreateView
from .forms import ReviewForm
from django.http import HttpResponseRedirect
import unicodedata
import re

def books_by_genre(request, genre):
    books = models.Book.objects.filter(genre=genre)
    return render(request, 'products/bookGenreResult.html', {'books': books, 'genre': genre})


def get_book_by_author(request, author_id):
    author = models.Author.objects.filter(pk=author_id)
    books = models.Book.objects.filter(author_id=author_id)
    return render(request,'products/bookAuthorResult.html', {'books': books, 'author': author})


def get_book_review(request):
    return render(request, 'products/bookReview.html')


def get_book_details(request,title):
    book = models.Book.objects.get(title=title)
    book_by_author = models.Book.objects.filter(author_id=book.author.id)
    reviews = models.Review.objects.filter(book_id=book.id)
    return render(request, 'products/bookDetail.html', {'book': book, 'book_by_author': book_by_author, 'reviews':reviews})

def order_author(request):
    search_request = request.GET.get('bookSearch')
    author = models.Book.objects.filter(Q(author__first_name__startswith= search_request) )
    author=author.all().order_by('author__first_name')
    return render(request,'products/bookAuthorResult.html', {'books': author, 'search_request': search_request})

def rating(request):
    search_request = request.GET.get('bookSearch')
    ratings = models.Book.objects.filter(Q(rating__icontains=search_request) | Q(rating__contains=search_request))
    ratings=ratings.all().order_by('-rating')
    return render(request, 'products/RatingSearchResult.html', {'books': ratings, 'search_request': search_request})

def search(request):
    search_request = request.GET.get('bookSearch')
    books = models.Book.objects.filter(
        Q(title__icontains=search_request) | Q(title__contains=search_request)|
        Q(author__first_name=search_request) | Q(author__last_name=search_request)|
    Q(rating__icontains=search_request) | Q(rating__contains=search_request)
    ).distinct()
    return render(request, 'products/bookSearchResult.html', {'books': books, 'search_request': search_request})

#########################################################################################################
##                                   REVIEW FUNCTIONS                                                  ##
########################################################################################################

def add_book_review(request):
    # get parameters from quantity form
    user_id = request.user.user_id
    user_rating = request.POST.get('user_rating')
    review_header = request.POST.get('review_header')
    review_body = request.POST.get('review_body')
    anonymous = request.POST.get('anonymous')
    book_id = request.POST.get('book_id')

    # add order item to database
    add_review = models.Review.objects.create(book_id=book_id, user_id=user_id, user_rating=user_rating,
                                        review_header=review_header, review_body=review_body,
                                        anonymous=anonymous)
    add_review.save()

    return HttpResponseRedirect(request.POST.get('next'))

#########################################################################################################
##                                   Joshua Functions                                                  ##
########################################################################################################

