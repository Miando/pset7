from django import forms
from .models import Stock
class QuoteForm(forms.Form):
    symbol = forms.CharField(max_length=100)

    class Meta:
        fields = ['symbol']


class BuyForm(forms.ModelForm):

    class Meta:
        model = Stock

        fields = ['symbol', 'shares']









