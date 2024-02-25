from django import forms
from .models import Commande


class FormulaireDeCC(forms.ModelForm):
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control rounded-3 shadow', 'placeholder': 'Email'}))
    nom = forms.CharField(label='Nom', max_length=50, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-3 shadow', 'placeholder': 'nom et prenom'}))
    adresse = forms.CharField(label='Adresse', max_length=50, required=True, widget=forms.Textarea(attrs={
        'class': 'form-control rounded-3 shadow', 'placeholder': 'adresse', 'rows': 2}))
    telephone = forms.CharField(label='Telephone', max_length=12, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-3 shadow', 'placeholder': 'Telephone'}))
    code_postal = forms.CharField(label='Code postal', max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-3 shadow', 'placeholder': 'code postal'}))
    ville = forms.CharField(label='Ville', max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control rounded-3 shadow', 'placeholder': 'ville'}))

    class Meta:
        model = Commande
        exclude = ['utilisateur']  # Exclude the utilisateur field, as it's a ForeignKey relationship
