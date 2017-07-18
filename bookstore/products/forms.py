from django.forms import ModelForm
from django import forms
from .models import Review


class ReviewForm(ModelForm):
    book_id = forms.CharField(widget=forms.HiddenInput())
    user_rating = forms.DecimalField(label='Rating', max_digits=3, decimal_places=2)
    review_header = forms.CharField(label="Review Heading", max_length=255)
    review_body = forms.CharField(label="Review Body")
    anonymous = forms.BooleanField(label="Anonymous")

    class Meta:
        model = Review
        fields = ['book_id', 'user_rating', 'review_header', 'review_body', 'anonymous']
