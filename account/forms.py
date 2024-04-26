from django import forms
from .models import Utilisateur
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class FormulaireDeConnexion(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    mdp = forms.CharField(label='Mot de passe',
                          widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class MdpChangeFormulaire(forms.Form):
    ancien_mdp = forms.CharField(label='Ancien mot de passe',
                                 widget=forms.PasswordInput(
                                     attrs={'class': 'form-control', 'placeholder': 'Ancien mot de passe'}))
    nouveau_mdp = forms.CharField(label='Nouveau mot de passe',
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'}))
    confirmer_mdp = forms.CharField(label='Confirmer le nouveau mot de passe',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Confirmer mot de passe'}))


class MdpResetFormulaire(forms.Form):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))


class MdpReinitFormulaire(forms.Form):
    nouveau_mdp = forms.CharField(label='Nouveau mot de passe',
                                  widget=forms.PasswordInput(
                                      attrs={'class': 'form-control', 'placeholder': 'Nouveau mot de passe'}))
    confirmer_mdp = forms.CharField(label='Confirmer le nouveau mot de passe',
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control', 'placeholder': 'Confirmer mot de passe'}))


class FormulaireEnregistrement(forms.ModelForm):
    nom = forms.CharField(label='Nom',
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
    prenom = forms.CharField(label='Prénom',
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    mdp = forms.CharField(label='Mot de passe',
                          widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
    mdp_2 = forms.CharField(label='Confirmer le mot de passe',
                            widget=forms.PasswordInput(
                                attrs={'class': 'form-control', 'placeholder': 'Confirmer mdp'}))
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(
        api_params={'hl': 'cl', 'onload': 'onLoadFunc'}
    ))

    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'email', 'date_naissance', 'image']

    def clean_mdp_2(self):
        cd = self.cleaned_data
        if cd['mdp'] != cd['mdp_2']:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cd['mdp_2']


class ProfileFormulaire(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    nom = forms.CharField(label='Nom', max_length=30, required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
    prenom = forms.CharField(label='Prenom', max_length=30, required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prenom'}))
    date_naissance = forms.DateField(required=False,
                                     widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date',
                                                                   'placeholder': 'date de naissance'}))
    image = forms.ImageField(required=False,
                             widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    adresse = forms.CharField(label='Adresse', max_length=50, required=False,
                              widget=forms.TextInput(
                                  attrs={'class': 'form-control', 'row': 2, 'placeholder': 'Adresse'}))
    telephone = forms.CharField(label='Telephone', max_length=12, required=False,
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telephone'}))
    ville = forms.CharField(label='Ville', max_length=30, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ville'}))
    code_postal = forms.CharField(label='Code Postal', max_length=30, required=False,
                                  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Code postal'}))

    class Meta:
        model = Utilisateur
        fields = ['email', 'nom', 'prenom', 'date_naissance', 'adresse', 'ville', 'telephone', 'image']
