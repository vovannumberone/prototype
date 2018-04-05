from django import forms
from django.contrib.auth.models import User
from postmaker.models import *

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
