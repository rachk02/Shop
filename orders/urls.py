from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('creer_commande/', views.creer_commande, name='creer_commande'),
    path('admin/commande/<int:id_commande>/pdf/', views.admin_commande_pdf, name='admin_commande_pdf'),
    path('commandes/', views.liste_commandes, name='liste_commandes'),
    path('commandes/<int:id>/', views.commande_detail, name='commande_detail'),
    path('commandes/<int:id_commande>/pdf/', views.commande_pdf, name='commande_pdf'),
]
