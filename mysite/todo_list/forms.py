from decimal import Decimal
from django import forms
from .models import Coin
from bootstrap_modal_forms.forms import BSModalForm


class CoinPopupForm(BSModalForm):
    quantity = forms.IntegerField(min_value=1)
    usa_price = forms.DecimalField(min_value=Decimal('0.01'))

    class Meta:
        model = Coin
        exclude = ['updated_at']


class CoinForm(forms.ModelForm):
    quantity = forms.IntegerField(min_value=1)
    usa_price = forms.DecimalField(min_value=Decimal('0.01'))

    class Meta:
        model = Coin
        fields = ('country', 'currency_name', 'currency_value', 'quantity',
                  'realse_year_ad', 'realse_year_ah', 'km', 'metal_type', 'usa_price',
                  'catalog_price', 'pick_number', 'serial_number', 'category', 'remarks', 'print_city')


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
    print_city = forms.CharField(required=False)

