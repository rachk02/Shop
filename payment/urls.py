from django.urls import path
from . import views
from . import webhooks

app_name = 'payment'

urlpatterns = [
    path('processus_de_paiement/', views.processus_de_paiement, name='processus_de_paiement'),
    path('paiement_unique/<int:id_commande>', views.paiement_unique, name='paiement_unique'),
    path('paiement_reussi/', views.paiement_reussi, name='paiement_reussi'),
    path('paiement_annuler/', views.paiement_annuler, name='paiement_annuler'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook')
]
