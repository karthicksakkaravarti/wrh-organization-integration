from django import forms
from django.contrib.auth.forms import AuthenticationForm
from turnstile.fields import TurnstileField


class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input block w-full'}, ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input block w-full'}))
    turnstile = TurnstileField()
