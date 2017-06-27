from django.forms import ModelForm
from django import forms
from .models import CreditCard


class EditCreditCart(ModelForm):
    name_on_card = forms.CharField(label='Name On Card', max_length=150)
    card_number = forms.CharField(label='Card Number', max_length=16)
    security_code = forms.CharField(label='Security Code', max_length=3)
    expiration_date = forms.DateField(label='Expiration Date')

    class Meta:
        model = CreditCard
        fields = ['name_on_card', 'cc_number', 'security_code', 'expiration']
