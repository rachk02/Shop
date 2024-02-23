from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def reset_link(utilisateur):
    uid = urlsafe_base64_encode(force_bytes(utilisateur.pk))
    token = default_token_generator.make_token(utilisateur)
    link = reverse('account:mdp_reinit', args=[uid, token])
    return link


def mdp_reinit_email(utilisateur, lien):
    objet = 'Réinitialisation du mot de passe'
    prenom_capitalized = utilisateur.prenom.split()
    prenom_capitalized = ' '.join([prenom.capitalize() for prenom in prenom_capitalized])

    nom_upper = utilisateur.nom.upper()
    message = render_to_string('account/mdp_re-init_email.html', {
        'email': utilisateur.email,
        'lien': lien,
        'username': f'{prenom_capitalized} {nom_upper}'
    })
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [utilisateur.email]
    send_mail(objet, message, from_email, to_email, fail_silently=False, html_message=message)
