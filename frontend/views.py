from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.http import JsonResponse
from .forms import InscriptionForm, LoginForm 
import re
from Wasangari.settings import EMAIL_HOST_USER
from .token import generatorToken

from django.contrib.sites.shortcuts import get_current_site
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.contrib import messages


def acceuil(request):
    form = InscriptionForm()
    login = LoginForm()
    return render(request, 'acceuil.html', {"form": form, "login": login})

def apprendre(request):
    # l'instruction ci-dessous récupère l'ensemble des cours
    cours = Cours.objects.all()

    # l'iNstruction ci-dessous récupère l'ensemble des cours associés thématiques
    cours_data = Cours.objects.prefetch_related('thematiques').all()
    # Dictionnaire contenant les cours et leurs thématiques associées
    cours_thematiques_dict = {
        cours.id: list(cours.thematiques.values_list('id', flat=True))
        for cours in cours_data
    }

    #l'instruction ci-dessous récupère lensemble de langues
    langues = Langues.objects.all()

    #l'instruction ci-dessous pour récupérer l'ensemble des thématiques
    thematiques = Thematique.objects.all()
    
    return render(request, 'apprendre.html', {"cours": cours, "thematiques":thematiques, "langues": langues})

@login_required
def chants_danses(request):
    return render(request, 'chants_danses.html')

@login_required
def ethnies(request):
    return render(request, 'ethnies.html')

@login_required
def langues(request):
    return render(request, 'langues.html')

@login_required
def gastronomie(request):
    return render(request, 'gastronomie.html')

@login_required
def divinites(request):
    return render(request, 'divinites.html')

@login_required
def royaumes(request):
    return render(request, 'royaumes.html')

@login_required
def patrimoines(request):
    return render(request, 'patrimoines.html')

def learn_something(request):
    return render(request, 'detail_cours.html')

def lecon (request):
    return  render(request, 'lecon.html')

@login_required
def decouvrir(request):
    return render(request, 'decouvrir.html')

def test(request):
    return render(request, 'testfontawesome.html')

@login_required
def sites(request):
    return render(request, 'sitehistorique.html')

@login_required
def monuments(request):
    return render(request, 'monuments.html')

@login_required
def musees(request):
    return render(request, 'musees.html')

@login_required
def parcs(request):
    return render(request, 'parcs.html')

@login_required
def reserve(request):
    return render(request, 'reserves.html')

@login_required
def acheter(request):
    return render(request, 'acheter.html')
@login_required
def meeting_details(request):
    return render(request, 'meeting-details.html')

@login_required
def evenements(request):
    return render(request, 'evenements.html')

@login_required
def explorer(request):
    return render(request, 'explorer.html')

#Vue d'inscription
def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST, request.FILES)
        loginform = LoginForm() 
        if form.is_valid():
            #Création de l'utilisateur
            #ethnie = Ethnies.objects.get(id=form.ethnie)
            last_name = form.cleaned_data['last_name']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            sexe = form.cleaned_data['sexe']
            ethnie = form.cleaned_data['ethnie']
            photo_de_profil = form.cleaned_data['photo_de_profil']

            try:
                user = User.objects.create_user(last_name = last_name, first_name = first_name, email=email, sexe = sexe, ethnie = ethnie, photo_de_profil = photo_de_profil)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "Inscription réussie !")
                # Email de bienvenue
                #envoyer_email(
                #    "E-mail de bienvenue",
                #    f"Bonjour {user.first_name} {user.last_name}, bienvenue sur Wassangari.",
                #    [user.email]
                #)
                # Email de confirmation
                #current_site = get_current_site(request)
                #email_subject = "Confirmation de votre adresse e-mail"
                #messageConfirm = render_to_string("emailconfirm.html", {
                #    "name": user.last_name,
                #    "domain": current_site,
                #    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                #    "token": generatorToken.make_token(user),
                #})
                #envoyer_email(email_subject, messageConfirm, [user.email])
                
                return redirect("acceuil")
            except Exception as e:
                messages.error (request, f"Une erreur s'est produite: {e} Veuillez réessayer l'inscription !")
                return render(request, 'acceuil.html', {'form': form, 'login': loginform, 'messages':e})
        else:
            messages.error(request, "Formulaire invalide !") 
            return render(request, 'acceuil.html', {'form': form, 'login': loginform, 'messages':e})

#Vue de connexion
def connexion(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        form = InscriptionForm()
        
        if login_form.is_valid():
            email = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(request, email = email, password = password)
            if user is not None:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect('acceuil')                  
            else:
                messages.error(request, "Adresse e-mail ou mot de passe incorrect !")
                return render(request, 'acceuil.html', {"form": form, "login": login_form})
        else:
            messages.error(request, "Formulaire de connexion invalide !")
            return render(request, 'acceuil.html', {"form": form, "login": login_form})

    else:
        return redirect("acceuil")

#fonction python pour envoyer un e-mail
def envoyer_email(subject, message, recipient_list):
    email = EmailMessage(subject, message, EMAIL_HOST_USER, recipient_list)
    email.fail_silently = False
    email.send()
     

#fonction d'activation d'email
def activate(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64), encoding='utf-8')
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generatorToken.check_token(user, token):
        user.is_active = True
        user.save()
        comment = "Félicitation, votre compte a bien été activé !"
        return render(request, 'connexion.html', {'comment': comment})
    else:
        messages.error(request, "La confirmation a échoué")
        return redirect('index')

@login_required 
def deconnexion(request):
    logout(request)
    messages.success(request, 'Vous avez bien été déconecté')
    return redirect('acceuil')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {})

@login_required
def article_c_d(request):
    return render(request, 'article_chants_danses.html')

@login_required
def article_ethnie(request):
    return render(request, 'articles_ethnies.html')

@login_required
def articles_langues(request):
    return render(request, 'articles_langues.html')

@login_required
def articles_gastronomie(request):
    return render(request, 'articles_gastronomie.html')

@login_required
def articles_divinites(request):
    return render(request, 'articles_divinites.html')

@login_required
def articles_royaumes(request):
    return render(request, 'articles_royaumes.html')

@login_required
def articles_patrimoines(request):
    return render(request, 'articles_patrimoines.html')