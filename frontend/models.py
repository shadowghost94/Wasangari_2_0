from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import os

#modèle de base utilisé pour la création du superutilisateur ou de l'utiliisateur par défaut
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

#modèle de base des objets de types ethnies
class Ethnies(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom de l'ethnie")
    description = models.TextField(verbose_name="Description")
    histoire = models.TextField(verbose_name="Histoire de l'ethnie")

    def __str__(self):
        return self.nom

class User(AbstractUser):
    SEXE = [
        ('Homme', 'Masculin'),
        ('Femme', 'Feminin')
    ]

    username = None
    email = models.EmailField(verbose_name="Adresse E-mail", unique=True)
    sexe = models.CharField(max_length=10, choices=SEXE, verbose_name="SEXE")
    ethnie = models.ForeignKey(Ethnies, on_delete=models.DO_NOTHING, blank=True, null = True)
    photo_de_profil = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Votre photo de profil")
    is_registered = models.BooleanField(default=0, verbose_name="Si l'utilisateur courant est inscrit pour un cours précis")
    profession = models.CharField(max_length=255, default="Historien, Enseignant chercheur à L'université de Parakou")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 

    def __str__(self):
        return self.first_name+" "+self.last_name

#modèle de base pour les objets de types Langues
class Langues(models.Model):
    nom = models.CharField(max_length=255, verbose_name="Nom de la langue")
    ethnie = models.ForeignKey(Ethnies, on_delete=models.DO_NOTHING, related_name="langues")

    def __str__(self):
        return self.nom
    
#modèle de base de données pour enregistrer des podcast
class Podcast(models.Model):
    APPARTENANCE = [
        ('apprendre', 'apprendre'),
        ('decouvrir', 'decouvrir'),
    ]
    titre = models.CharField(max_length=255, verbose_name="Titre de l'article")
    description = models.TextField(verbose_name="Une petite description de votre podcast")
    date_et_heure = models.DateTimeField(auto_now=True)
    podcast_profil = models.ImageField(upload_to='podcast_pictures/', blank=True, null=True, verbose_name="Ajouter une photo")
    appartenance = models.CharField(max_length=12, choices=APPARTENANCE, verbose_name="sexion d'appartenance du podcast")

class Evenement(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    lieu = models.CharField(max_length=255)
    statut = models.CharField(max_length=55)
    prix_entree = models.DecimalField(max_digits=10, decimal_places=2)
    nbr_places_dispo = models.IntegerField()
    media_profil_url = models.ImageField(upload_to='photo_evenement/', null=True, blank=True, default='default.jpg')

    def __str__(self):
        return self.nom
    
class ObjetVente(models.Model):
    titre = models.CharField(max_length=64)
    auteur = models.CharField(max_length=64)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    media_url = models.ImageField(upload_to='photo_objetVente/', null=True, blank=True, default='photo_objetVente/default.jpg')

    def __str__(self):
        return self.titre
    
class Thematique(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.nom

class Cours(models.Model):
    DISPONIBILITE = [
        ('ouvert', 'Ouvert pour inscription'),
        ('bientot', 'Bientôt'),
        ('en_cours', 'En cours'),
        ('archive', 'Archivé')
    ]

    titre = models.CharField(max_length=255)
    objectif = models.CharField(max_length=255, verbose_name="En une ou deux phrases, en quoi ce cours sera utile pour la personne qui le suivra ?", default="Que vous ayez déjà suivi le MOOC de l’an passé ou pas, ce MOOC est fait pour vous afin de rester employable et IA compatible alors que tout va si vite !")
    description = models.TextField()
    langue = models.ForeignKey(Langues, on_delete=models.DO_NOTHING)
    date_et_heure = models.DateTimeField(auto_now=True)
    duree = models.IntegerField(verbose_name="Durée total de l'apprentissage (en nombre de semaine)", default=4)
    effort = models.IntegerField(verbose_name="Effort à fournir en dehors des heures de cours (en nombre d'heures)", default=12)
    rythme = models.IntegerField(verbose_name="Rythme d'apprentissage du cours (en nombre d'heure) par semaine", blank=True, null=True)
    certifiante = models.BooleanField(default=False)
    photo_de_profil = models.ImageField(upload_to='courses_pictures/', blank=True, null=True, verbose_name="Une image de description pour le cours")
    videos = models.FileField(upload_to="", blank=True, null=True, verbose_name="Une vidéo eplicatif du cours, pour donner un avant goût à l'apprenant")
    a_apprendre = models.TextField()
    glossaire = models.TextField()
    nombre_semaine = models.IntegerField(default=1, verbose_name="Durée de l'apprentissage en nombre de semaine")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    thematiques = models.ManyToManyField(Thematique, related_name='cours', blank=True)
    disponibilite = models.CharField(max_length=24, choices=DISPONIBILITE, verbose_name="Disponibilité du cours")
    format = models.TextField(verbose_name="Le format du cours, Comment le cours est divisé ? Combien de semaine ? Est-ce qu'il y aura des lives ? A quel rythme ?", default="")
    prerequis = models.TextField(verbose_name="Les pré-requis nécessaire pour suivre le cours", default="")
    evaluation_certification = models.TextField(verbose_name="Comment les apprenants seront évalués ? Est-ce qu'ils auront une certification à la fin ?", default="")

    def __str__(self):
        return self.titre

class Semaine(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Donner un titre pour l'ensemble des notions à apprendre durant cette semaine")
    nombre_lecon = models.IntegerField(verbose_name="Nombre de leçon pour la semaine")
    cours = models.ForeignKey(Cours, on_delete=models.DO_NOTHING, default="X", related_name = "cours")

    def __str__(self):
        return self.titre

def lecon_file_path(instance, filename):
    """Crée un répertoire unique basé sur l'ID de la leçon ou du cours"""
    return os.path.join(f'course_videos/lecon_{instance.id}', filename)


class Lecon(models.Model):
    date_et_heure = models.DateTimeField(auto_now=True)
    titre = models.CharField(max_length=255, verbose_name="Donner un titre pour cette leçon que vous souhaitez ajouter")
    video = models.FileField(upload_to=lecon_file_path, verbose_name="Ajouter la version vidéo de la leçon", default="X")
    pdf = models.FileField(upload_to=lecon_file_path, verbose_name="Ajouter la/les fichiers de documentation qui accompagne la vidéo")
    semaine = models.ForeignKey(Semaine, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

#Modele gerant l'inscription des utilisateurs
class Inscription(models.Model):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validée'),
        ('annulee', 'Annulée')
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    cours = models.ForeignKey(Cours, on_delete=models.CASCADE)
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=10, choices=STATUT_CHOICES, default='en_attente')

    class Meta:
        unique_together = ('utilisateur', 'cours')  # Empêche un utilisateur de s'inscrire plusieurs fois au même cours

    def __str__(self):
        return f"{self.utilisateur.username} - {self.cours.titre}"