from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Commande


@shared_task
def paiement_reussi(id_commande):
    commande = Commande.objects.get(id=id_commande)

    objet = f'Commande n° {commande.generer_numero_commande()}'
    html_message = render_to_string('orders/commande_mail.html',
                                    {
                                        'username': f'{commande.utilisateur.prenom.lower()} {commande.utilisateur.nom.upper()}',
                                        'commande': commande,
                                        'total': commande.cout_total()})
    email = EmailMessage(objet, html_message, settings.DEFAULT_FROM_EMAIL, [commande.utilisateur])
    email.content_subtype = "html"

    envoi_mail = email.send()
    return envoi_mail
