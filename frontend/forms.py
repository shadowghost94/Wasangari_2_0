from django import forms
from django.core.validators import EmailValidator
from .models import User
import re

class InscriptionForm(forms.ModelForm):
    email = forms.EmailField(validators=[EmailValidator()], required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'E-MAIL',
        'class': 'form-control',
        'id': 'email',
    }),
    label=' ')
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'password',
            'placeholder': 'MOT DE PASSE',
            'class': 'form-control'
        }),
        label=' '
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'id': 'password-confirm',
            'placeholder': 'CONFIRMER MOT DE PASSE',
            'class': 'form-control',
            
        }),
        label=' '
    )

    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email', 'sexe', 'ethnie', 'photo_de_profil',]
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'NOMS',
                
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'PRENOMS'
            }),
            
            'sexe': forms.Select(attrs={
                'class': 'form-control',
                'id': 'sexe'
            }),
            'ethnie':forms.Select(attrs={
                'class': 'form-control',
                'id': 'ethnie'
            }),
            'photo_de_profil': forms.FileInput(attrs={
                'class': 'form-control',
                'id': '',
                'accept': 'image/*',
                'upload_to': 'profile_pictures/'
            })
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("confirm_password")

        #vérification si e-mail existe
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un utilisateur avec cet e-mail existe déjà.")
    
        #vérification si les deux password correspondent
        if password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")
        
        #vérification si mot de passe est un mot de passe solide
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")
    
    #cette méthode permet de définir le label de chaque champ à null
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].label = ' ' 

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