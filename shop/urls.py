from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('produits/', views.produit_list, name='produit_list'),
    path('marques/', views.marque_list, name='marque_list'),
    path('categories/', views.categorie_list, name='categorie_list'),
    path('marques/<slug:marque_slug>/', views.produit_list_marque, name='produit_list_marque'),
    path('categories/<slug:categorie_slug>/', views.produit_list_categorie, name='produit_list_categorie'),
    path('marques/<slug:marque_slug>/<slug:categorie_slug>/', views.produit_list_marque_categorie, name='produit_list_marque_categorie'),
    path('produits/<int:id>/<slug:slug>/', views.produit_detail, name='produit_detail'),
]
