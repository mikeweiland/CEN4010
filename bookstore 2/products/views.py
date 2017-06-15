from django.shortcuts import render
from django.db.models import Q
from . import models

def booksByGenre(request,genre):
    books = models.Book.objects.filter(genre=genre)
    return render(request,'products/bookResults.html',{'books':books})

def search(request):
    searchRequest = request.GET.get('bookSearch')
    books = models.Book.objects.filter(
        Q(title__icontains=searchRequest)| Q(title__contains=searchRequest)
    )
    return render(request, 'products/bookResults.html', {'books':books})

