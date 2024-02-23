from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.panier_detail, name='panier_detail'),
    path('ajouter/<int:id_produit>/', views.ajouter_produit,
         name='ajouter_produit'),
    path('ajouter-un/<int:id_produit>/', views.ajouter_produit_direct,
         name='ajouter-un'),
    path('retirer/<int:id_produit>/', views.retirer_produit,
         name='retirer_produit'),
    path('maj/<int:id_produit>/', views.maj_quantite,
         name='maj_quantite')
]
