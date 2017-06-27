from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("nickname","email_address","password1","password2")
        model = get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["email_address"].label = "Email Address"


class EditUserProfileForm(ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    nickname = forms.CharField(label='Nickname')
    email_address = forms.CharField(label="Email Address")

    class Meta:
        model = User
        fields = ['first_name', 'last_name','nickname','email_address']

