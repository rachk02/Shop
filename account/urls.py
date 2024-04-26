from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('connexion/', views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('mdp_reinit_dem/', views.mdp_reinit_dem, name='mdp_reinit_dem'),
    path('mdp-reinit/<str:uid>/<str:token>/', views.mdp_reinit, name='mdp_reinit'),
    path('mdp_change/', views.mdp_change, name='mdp_change'),
    path('compte_creation/', views.compte_creation, name='compte_creation'),
    path('activation/<str:uidb64>/<str:token>/', views.compte_activation, name='compte_activation'),
    path('activation_reussi/', views.activation_reussi, name='activation_reussi'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
]
