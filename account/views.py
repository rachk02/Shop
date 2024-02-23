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


marques = Marque.objects.all()
categories = Categorie.objects.all()
m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)


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
                   'utilisateur': request.user})


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
                   'utilisateur': request.user})


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
                   'utilisateur': request.user})


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
                      {'formulaire': formulaire, 'utilisateur': request.user, 'lien': lien})
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
            login(request, utilisateur)
            messages.success(request, 'Votre compte a été créé avec succès. Bienvenue !')
            return redirect('shop:homepage')
    else:
        formulaire = FormulaireEnregistrement()

    return render(request, 'account/compte_creation.html',
                  {'formulaire': formulaire,
                   'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user})


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
                  {'formulaire': formulaire,
                   'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user})
