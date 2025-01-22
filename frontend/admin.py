from django.contrib import admin
from .models import User, Ethnies, Langues, Cours, Thematique

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "email", "sexe", "photo_de_profil")
    search_fields = ("email", "last_name", "prenoms")

class EthniesAdmin(admin.ModelAdmin):
    list_display = ("nom", "description", "histoire")

class LanguesAdmin(admin.ModelAdmin):
    list_display = ("nom", "ethnie")

class CoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'description', 'langue', 'photo_de_profil')

class UserThematique(admin.ModelAdmin):
    list_display = ('nom', 'description')

admin.site.register(Thematique, UserThematique)
admin.site.register(User, UserAdmin)
admin.site.register(Ethnies, EthniesAdmin)
admin.site.register(Langues, LanguesAdmin)
admin.site.register(Cours, CoursAdmin)