from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import JsonResponse
from .forms import LoginForm 
import re
from Wasangari.settings import EMAIL_HOST_USER
from .token import generatorToken

from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.contrib import messages


def acceuil(request):
    return render(request, 'acceuil.html')

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

def learn_something(request, cours_id):
    cours_id = cours_id
    cours = Cours.objects.get(id=cours_id)
    thematiques_du_cours = cours.thematiques.all()
    langue = Langues.objects.get(id=cours.langue_id)

    #On vérifie si l'utilisateur courant est déjà inscrit pour le cours auquel il éssaye d'accéder
    cours = get_object_or_404(Cours, id=cours_id)
    is_registered = Inscription.objects.filter(utilisateur=request.user, cours=cours).exists()

    #On récupère la ligne a_apprendre et on on le separe en plusieurs phrases grâe au point virgule
    ce_qua_apprendre = cours.a_apprendre.split(";")
    format = cours.format.split(";")

    return render(request, 'detail_cours.html', {'cours': cours, 'thematiques': thematiques_du_cours, 'langue': langue, 'is_registered': is_registered, 'user': request.user, 'ce_qua_apprendre': ce_qua_apprendre, 'format': format})

@login_required
def lecon (request, coursid):
    coursid = coursid
    cours = Cours.objects.get(id=coursid)
    semaines = Semaine.objects.filter(cours_id=cours.id)
    lecons = Lecon.objects.filter(semaine__in=semaines)

    return  render(request, 'lecon.html', {'cours':cours, 'semaines': semaines, 'lecons': lecons})

@login_required
def decouvrir(request):
    return render(request, 'decouvrir0.html')

@login_required
def decouvrirarticle(request):
    return render(request, 'decouvrirarticle.html')

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
        try:
            # Récupération des données
            nom = request.POST.get('nom')
            prenom = request.POST.get('prenom')
            email = request.POST.get('email')
            sexe = request.POST.get('sexe')
            langue =Langues.objects.get(pk=int(request.POST.get('langue')))
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            photo = request.FILES.get('photo')
            
            # Validation
            if not all([nom, prenom, email, password, confirm_password]):
                return JsonResponse({'success': False, 'message': 'Tous les champs obligatoires doivent être remplis'})
                
            if password != confirm_password:
                return JsonResponse({'success': False, 'message': 'Les mots de passe ne correspondent pas'})
                
            if len(password) < 8:
                return JsonResponse({'success': False, 'message': 'Le mot de passe doit contenir au moins 8 caractères'})
            
            # Création de l'utilisateur
            user = User.objects.create(
                first_name=prenom,
                last_name=nom,
                email=email,
                password=make_password(password),
                sexe=sexe,
                langues=langue
            )
            
            if photo:
                user.photo_de_profil.save(photo.name, photo)
            
            return JsonResponse({'success': True, 'message': 'Inscription réussie'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        
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

    else:
        langues = Langues.objects.all()
        return render(request, "inscription.html", {'langues': langues})
    
#Vue de connexion
def connexion(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        
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
                return render(request, 'acceuil.html')
        else:
            messages.error(request, "Formulaire de connexion invalide !")
            return render(request, 'acceuil.html')

    else:
        login_form = LoginForm()
        return render(request, "connexion.html", {'login': login_form})

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

@login_required
def registered_user(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    inscription, created = Inscription.objects.get_or_create(utilisateur=request.user, cours=cours)

    if created:
        messages.success(request, "Vous avez bien été inscrit pour le cours !")
    else:
        messages.warning(request, "Vous êtes déjà inscrit à ce cours !")

    return redirect('detail-cours', cours_id=cours.id)

@login_required
def unregistered_user(request, cours_id):
    cours = get_object_or_404(Cours, id=cours_id)
    inscription = Inscription.objects.filter(utilisateur=request.user, cours=cours).first()

    if inscription:
        inscription.delete()
        messages.success(request, "Vous avez bien été désinscrire du cours !")
    else:
        messages.warning(request, "Vous n'êtes pas inscrit à ce cours !")

    return redirect('detail-cours', cours_id=cours.id)