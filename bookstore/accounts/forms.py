from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from .models import User, Address
from django.core.validators import validate_email


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("nickname","email_address", 'first_name', 'last_name', "password1","password2")
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["email_address"].label = "Email Address"
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"


class EditUserProfileForm(ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    nickname = forms.CharField(label='Nickname')
    email_address = forms.EmailField(label="Email Address")

    class Meta:
        model = User
        fields = ['first_name', 'last_name','nickname','email_address']


class AddressForm(ModelForm):
    street_address = forms.CharField(max_length=255, label="Street Address")
    city = forms.CharField(max_length=50, label="City")
    state = forms.CharField(max_length=2, label="State")
    zip_code = forms.CharField(max_length=5, label="Zip Code")

    class Meta:
        model = Address
        fields = ['street_address','city','state','zip_code']


