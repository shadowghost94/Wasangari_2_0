from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

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
    description = models.TextField()
    langue = models.ForeignKey(Langues, on_delete=models.DO_NOTHING)
    date_et_heure = models.DateTimeField(auto_now=True)
    photo_de_profil = models.ImageField(upload_to='courses_pictures/', blank=True, null=True, verbose_name="Une image de description pour le cours")
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    thematiques = models.ManyToManyField(Thematique, related_name='cours', blank=True)
    disponibilite = models.CharField(max_length=24, choices=DISPONIBILITE, verbose_name="Disponibilité du cours", default="En cours")

class Lecon(models.Model):
    titre = models.CharField(max_length=255)
    date_et_heure = models.DateTimeField(auto_now=True)
    video = models.FileField(upload_to='file_reference/', blank=True, null=True)
    pdf = models.FileField(upload_to="file_reference/", blank=True, null=True)
    cours = models.ForeignKey(Cours, on_delete=models.DO_NOTHING)

class A_Apprendre(models.Model):
    contenue = models.TextField()
    cours = models.ForeignKey(Cours, on_delete=models.DO_NOTHING)

