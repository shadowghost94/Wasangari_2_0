from django import forms
from django.core.validators import EmailValidator
from .models import User
import re

#formulaire de connexion
class LoginForm(forms.Form):
    username = forms.CharField(
        label=" ",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-MAIL',
        })
    )
    password = forms.CharField(
        label=" ",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'MOT DE PASSE',
        })
    )