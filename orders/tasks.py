from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import Commande
from django.conf import settings


@shared_task
def commande_passer(id_commande):
    commande = Commande.objects.get(id=id_commande)
    objet = f'Commande n° {commande.generer_numero_commande()}'

    # Charger le modèle HTML en tant que chaîne de texte
    html_message = render_to_string('orders/commande_mail.html',
                                    {'username': f'{commande.utilisateur.prenom.lower()} {commande.utilisateur.nom.upper()}',
                                     'commande': commande,
                                     'panier': commande.items.all(),
                                     'total': commande.cout_total()})

    # Envoyer l'email avec le contenu HTML
    email = EmailMessage(objet, html_message, settings.DEFAULT_FROM_EMAIL, [commande.email()])
    email.content_subtype = "html"

    # Envoyer l'email
    envoi_mail = email.send()
    return envoi_mail
