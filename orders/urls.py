from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('creer_commande/', views.creer_commande, name='creer_commande'),
]
