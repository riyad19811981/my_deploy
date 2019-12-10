from django import forms
from .models import List
from django.contrib.auth.models import User
from .models import UserProfileInfo


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        # fields=["item","completed"]
        # or
        fields = '__all__'
    # to bring all fields


class MyDjangoForm(forms.Form):
    name = forms.CharField(required=False)
    email = forms.EmailField()
    text = forms.CharField(widget=forms.Textarea)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ("portfolio_site", "profile_pic")
