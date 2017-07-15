from django.shortcuts import render
from django.db.models import Q
from django.urls import reverse
from . import models
from django.views.generic import CreateView
from .forms import ReviewForm


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
    return render(request, 'products/bookDetail.html', {'book': book, 'book_by_author': book_by_author})


def search(request):
    search_request = request.GET.get('bookSearch')
    books = models.Book.objects.filter(
        Q(title__icontains=search_request) | Q(title__contains=search_request)
    )
    return render(request, 'products/bookSearchResult.html', {'books': books, 'search_request': search_request})


#########################################################################################################
##                                   REVIEW FUNCTIONS                                                  ##
########################################################################################################

class ReviewCreate(CreateView):
    template_name = 'products/bookReview.html'
    model = models.Review
    form_class = ReviewForm

    def form_valid(self,form):
        form.instance.user = self.request.user
        form.save()
        return super(ReviewCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('next')


