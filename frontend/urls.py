from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.acceuil, name='acceuil'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('apprendre/', views.apprendre, name='apprendre'),
    path('apprendre/detail-cours/<int:cours_id>', views.learn_something, name='detail-cours'),
    path('apprendre/detail-cours/lecon/<int:coursid>', views.lecon, name="lecon"),
    path('decouvrir/', views.decouvrir, name='decouvrir'),
    path('decouvrir/detail-article/', views.decouvrirarticle, name="decouvrirdetailarticle"),
    path('sites/', views.sites, name='sites'),
    path('monuments/', views.monuments, name='monuments'),
    path('musees/', views.musees, name='musees'),
    path('parcs/', views.parcs, name='parcs'),
    path('reserve/', views.reserve, name='reserve'),
    path('acheter/', views.acheter, name='acheter'),
    path('explorer/', views.explorer, name='explorer'),
    path('meeting-details/', views.meeting_details, name='meeting-details'),
    path('evenements/', views.evenements, name='evenements'),
    path('dahsboard/', views.dashboard, name="dashboard"),
    path('detail_chants_danses/', views.chants_danses, name="chants_danses"),
    path('detail_ethnies/', views.ethnies, name="ethnies"),
    path('detail_langues/', views.langues, name="langues"),
    path('detail_gastronomie/', views.gastronomie, name="gastronomie"),
    path('detail_divinites/', views.divinites, name="divinites"),
    path('detail_royaumes/', views.royaumes, name="royaumes"),
    path('detail_patrimoines/', views.patrimoines, name="patrimoines"),
    path('article_chants_danses/', views.article_c_d, name="article_c_d"),
    path('article_ethnies/', views.article_ethnie, name="article_ethnie"),
    path('articles_langues/', views.articles_langues, name='articles_langues'),
    path('articles_gastronomie/', views.articles_gastronomie, name="articles_gastronomie"),
    path('articles_divinites/', views.articles_divinites, name="articles_divinites"),
    path('articles_royaumes/', views.articles_royaumes, name="articles_royaumes"),
    path('articles_patrimoines/', views.articles_patrimoines, name="articles_patrimoines"),
    path('test/', views.test, name="test"),
    path('apprendre/detail-cours/<int:cours_id>/registered_user', views.registered_user, name="registered_user"),
    path('apprendre/detail-cours/<int:cours_id>/unregistered_user', views.unregistered_user, name="unregistered_user")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)