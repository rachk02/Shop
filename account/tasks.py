from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from orders.models import Utilisateur


@shared_task
def confirmation(id_utilisateur, lien):
    try:
        utilisateur = Utilisateur.objects.get(id=id_utilisateur)
    except Utilisateur.DoesNotExist:
        print(f"L'utilisateur avec l'id {id_utilisateur} n'existe pas.")
        return None

    objet = 'Confirmation de votre identite'
    html_message = render_to_string('account/activation_mail.html',
                                    {'lien': lien})
    email = EmailMessage(objet, html_message, settings.DEFAULT_FROM_EMAIL, [utilisateur.email])
    email.content_subtype = "html"

    envoi_mail = email.send()
    return envoi_mail
