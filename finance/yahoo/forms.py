from django import forms
from .models import Stock
from django.contrib.auth.models import User

class QuoteForm(forms.Form):
    symbol = forms.CharField(max_length=100)

    class Meta:
        fields = ['symbol']


class BuyForm(forms.ModelForm):

    class Meta:
        model = Stock

        fields = ['symbol', 'shares']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']






