from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from .models import Utilisateur


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        u = sociallogin.user
        u.set_unusable_password()  # Si le mot de passe ne doit pas être utilisé

        # Exemple: récupération du prénom et du nom depuis les données supplémentaires du compte social
        # La structure des données peut varier selon le fournisseur
        extra_data = sociallogin.account.extra_data
        u.nom = extra_data.get('last_name', '')  # Utilisez les clés correctes pour votre cas
        u.prenom = extra_data.get('first_name', '')  # Utilisez les clés correctes pour votre cas

        if 'email' in extra_data:
            # S'assurer que l'email est mis à jour avec les données de sociallogin
            u.email = extra_data['email']

        # Sauvegarde de l'utilisateur
        u.save()
        # Vérifiez si l'objet sociallogin doit être enregistré après l'utilisateur
        sociallogin.save(request)

        # Optionnel: toucher ici des signaux de suivi ou des actions supplémentaires
        # Si vous avez une logique post-enregistrement ou post-connexion

        return u

    def pre_social_login(self, request, sociallogin):
        if not sociallogin.is_existing:
            # Vérifier s'il existe un utilisateur avec le même email
            email = sociallogin.user.email
            try:
                user = Utilisateur.objects.get(email=email)
                # Connecter le compte social à l'utilisateur existant
                sociallogin.connect(request, user)
            except Utilisateur.DoesNotExist:
                pass  # Pas d'action nécessaire si l'utilisateur n'existe pas

    def add_message(self, request, level, message_template,
                    message_context=None, extra_tags=''):
        # Ne fait rien, ignore les messages
        pass

    def get_signup_redirect_url(self, request):
        # Utilisez reverse() pour obtenir l'URL depuis le nom de la vue
        from django.urls import reverse
        return reverse('shop:homepage')  # Utiliser le bon espace de noms du nom de la vue
