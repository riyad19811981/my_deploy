from decimal import Decimal

from django import forms
from .models import List, Coin
from django.contrib.auth.models import User
from .models import UserProfileInfo


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        # fields=["item","completed"]
        # or
        fields = '__all__'
    # to bring all fields


class CoinForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    usa_price = forms.DecimalField(min_value=Decimal('0.01'))

    class Meta:
        model = Coin
        fields = ('country', 'currency_name', 'currency_value', 'quantity',
                  'realse_year_ad', 'realse_year_ah', 'km', 'metal_type', 'usa_price',
                  'catalog_price', 'pick_number', 'serial_number', 'category', 'remarks')


class CoinFilterForm(forms.Form):
    country = forms.IntegerField(required=False)
    category = forms.IntegerField(required=False)
    currency_name = forms.CharField(required=False)
    currency_value = forms.CharField(required=False)
    realse_year_ad = forms.CharField(required=False)
    realse_year_ah = forms.CharField(required=False)
    km = forms.CharField(required=False)
    metal_type = forms.CharField(required=False)
    quantity = forms.CharField(required=False)
    usa_price = forms.CharField(required=False)
    catalog_price = forms.CharField(required=False)
    pick_number = forms.CharField(required=False)
    serial_number = forms.CharField(required=False)
    remarks = forms.CharField(required=False)


class MyDjangoForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    myfield1 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    myfield2 = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ("portfolio_site", "profile_pic")