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

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        # check if nickname submitted is the same as the current user online
        if nickname == self.instance.nickname:
            return nickname

        # username is different from previous, check if it already exists
        if User.objects.get(nickname=nickname):
            raise forms.ValidationError('Nickname already exists.')

        return nickname

    def clean_email_address(self):
        email_address = self.cleaned_data['email_address']
        print('The email address : ' + email_address)
        print('The email address : ' + self.instance.email_address)

        # check if email address submitted is the same as the current user online
        if email_address == self.instance.email_address:
            return email_address

        # email address is different from previous, check if it already exits
        try:
            User.objects.exclude(pk=self.instance.user_id).get(email_address=email_address)
        except User.DoesNotExist:
            return email_address

        raise forms.ValidationError('Email Address already exists')

    class Meta:
        model = User
        fields = ['first_name', 'last_name','nickname','email_address']


class AddressForm(ModelForm):
    street_address = forms.CharField(max_length=255, label="Street Address")
    city = forms.CharField(max_length=50, label="City")
    state = forms.CharField(max_length=2, label="State")
    zip_code = forms.CharField(max_length=5, label="Zip Code")

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if not zip_code.isdigit():
            raise forms.ValidationError('Zip Code can only contains numbers.')

        return zip_code

    def clean_state(self):
        state = self.cleaned_data['state']
        if not state.isalpha():
            raise forms.ValidationError('State can only contain letters.')

        return state

    class Meta:
        model = Address
        fields = ['street_address','city','state','zip_code']


