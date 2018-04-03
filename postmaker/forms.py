from django import forms
from django.contrib.auth.models import User
from postmaker.models import Account

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('user', 'publics')
