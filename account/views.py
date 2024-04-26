from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import FormulaireDeConnexion, MdpChangeFormulaire, MdpResetFormulaire, MdpReinitFormulaire, \
    FormulaireEnregistrement, ProfileFormulaire
from shop.models import Marque, Categorie
from .utils import reset_link, mdp_reinit_email
from .models import Utilisateur
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tasks import confirmation
from shop.forms import FormulaireRA

marques = Marque.objects.all()
categories = Categorie.objects.all()
m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)
formulaire_recherche = FormulaireRA()


def connexion(request):
    if request.method == 'POST':
        formulaire = FormulaireDeConnexion(request.POST)
        if formulaire.is_valid():
            email = formulaire.cleaned_data['email']
            mdp = formulaire.cleaned_data['mdp']
            utilisateur = authenticate(request, email=email, password=mdp)
            if utilisateur is not None:
                if utilisateur.is_active:
                    login(request, utilisateur)
                    messages.success(request, 'Connexion réussie.')
                    return redirect('shop:homepage')
                else:
                    messages.error(request, "Compte désactivé.")
                    return HttpResponse("Compte désactivé.")
            else:
                messages.error(request, "Connexion échouée. Veuillez vérifier votre email et votre mot de passe.")
                return HttpResponse("Connexion échouée, Veuillez vérifier votre email et votre mot de passe.")
    else:
        formulaire = FormulaireDeConnexion()
    return render(request, 'account/connexion.html',
                  {'formulaire': formulaire,
                   'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user,
                   'formulaire_recherche': formulaire_recherche,
                   })


@login_required
def deconnexion(request):
    logout(request)
    messages.success(request, 'Déconnexion réussie.')
    return redirect('shop:homepage')


@login_required
def mdp_change(request):
    if request.method == 'POST':
        formulaire = MdpChangeFormulaire(request.POST)
        if formulaire.is_valid():
            ancien_mdp = formulaire.cleaned_data['ancien_mdp']
            nouveau_mdp = formulaire.cleaned_data['nouveau_mdp']
            confirmer_mdp = formulaire.cleaned_data['confirmer_mdp']

            if not request.user.check_password(ancien_mdp):
                messages.error(request, 'L\'ancien mot de passe est incorrect.')
                return redirect('account:password_change')

            if nouveau_mdp != confirmer_mdp:
                messages.error(request, 'Les mots de passe sont différents.')
                return redirect('account:password_change')

            request.user.set_password(nouveau_mdp)
            request.user.save()

            update_session_auth_hash(request, request.user)

            messages.success(request, 'Votre mot de passe a été modifié avec succès.')
            return redirect('shop:homepage')
    else:
        formulaire = MdpChangeFormulaire()

    return render(request, 'account/mdp_change.html',
                  {'formulaire': formulaire,
                   'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user,
                   'formulaire_recherche': formulaire_recherche,
                   })


def mdp_reinit_dem(request):
    if request.method == 'POST':
        formulaire = MdpResetFormulaire(request.POST)
        if formulaire.is_valid():
            email = formulaire.cleaned_data['email']
            utilisateur = get_object_or_404(Utilisateur, email=email)

            lien = reset_link(utilisateur)

            mdp_reinit_email(utilisateur, lien)

            messages.info(request, f'Un lien de réinitialisation de mot de passe a été envoyé à {utilisateur.email}.')
            return redirect(reverse('shop:homepage'))
    else:
        formulaire = MdpResetFormulaire()

    return render(request, 'account/mdp_re-init_dem.html',
                  {'formulaire': formulaire,
                   'utilisateur': request.user,
                   'formulaire_recherche': formulaire_recherche,
                   })


def mdp_reinit(request, uid, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid))
        utilisateur = get_object_or_404(Utilisateur, pk=uid)
    except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
        utilisateur = None

    if utilisateur is not None and default_token_generator.check_token(utilisateur, token):
        if request.method == 'POST':
            formulaire = MdpReinitFormulaire(request.POST)
            if formulaire.is_valid():
                nouveau_mdp = formulaire.cleaned_data['nouveau_mdp']
                confirmer_mdp = formulaire.cleaned_data['confirmer_mdp']

                if nouveau_mdp != confirmer_mdp:
                    messages.error(request, 'Les mots de passe ne correspondent pas.')
                    return redirect('account:mdp_reinit')

                utilisateur.set_password(nouveau_mdp)
                utilisateur.save()

                messages.success(request, 'Votre mot de passe a été réinitialisé avec succès.')
                return redirect('shop:homepage')

        else:
            formulaire = MdpReinitFormulaire()

        lien = reset_link(utilisateur)

        return render(request, 'account/mdp_re-init.html',
                      {'formulaire_reinit': formulaire,
                       'utilisateur': request.user,
                       'lien': lien,
                       'formulaire': formulaire_recherche, })
    else:
        messages.error(request, 'Le lien de réinitialisation du mot de passe est invalide ou a expiré.')
        return redirect('shop:homepage')


def compte_creation(request):
    if request.method == 'POST':
        formulaire = FormulaireEnregistrement(request.POST)
        if formulaire.is_valid():
            utilisateur = formulaire.save(commit=False)
            utilisateur.set_password(formulaire.cleaned_data['mdp'])
            utilisateur.save()

            uid = urlsafe_base64_encode(force_bytes(utilisateur.pk))
            token = default_token_generator.make_token(utilisateur)

            lien_confirmation = reverse(
                'account:compte_activation',
                kwargs={'uidb64': uid, 'token': token}
            )
            lien_complet = request.build_absolute_uri(lien_confirmation)

            confirmation.delay(utilisateur.id, lien_complet)

            messages.success(request,
                             'Un email de confirmation vous a été envoyé. Veuillez vérifier votre boîte de réception.')
            return redirect('shop:homepage')
    else:
        formulaire = FormulaireEnregistrement()

    return render(request, 'account/compte_creation.html',
                  {'formulaire_create': formulaire,
                   'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user,
                   'formulaire_recherche': formulaire_recherche,
                   })


def compte_activation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        utilisateur = Utilisateur.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
        utilisateur = None

    if utilisateur is not None and default_token_generator.check_token(utilisateur, token):
        utilisateur.is_active = True
        utilisateur.save()
        login(request, utilisateur)
        return redirect('account:activation_reussi')
    else:
        return HttpResponse("Le lien d'activation est invalide ou a expiré.")


def activation_reussi(request):
    redirect_url = request.build_absolute_uri('shop:homepage')
    return render(request, 'account/activation_reussi.html',
                  {'redirect_url': redirect_url,
                   'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user,
                   'formulaire_recherche': formulaire_recherche,
                   })


@login_required
def profile_edit(request):
    if request.method == 'POST':
        formulaire = ProfileFormulaire(request.POST, request.FILES, instance=request.user)
        if formulaire.is_valid():
            formulaire.save()
            messages.success(request, 'Profil mis à jour avec succès.')
            return redirect('shop:homepage')
    else:
        formulaire = ProfileFormulaire(instance=request.user)

    return render(request, 'account/profile_edit.html',
                  {'formulaire_edit': formulaire,
                   'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user,
                   'formulaire_recherche': formulaire_recherche, })
