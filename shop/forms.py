from django import forms


class FormulaireRA(forms.Form):
    mot_cle = forms.CharField(
        label='',
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm rounded-4',
            'placeholder': '🔍 Rechercher',
            'aria-label': 'Rechercher'  # Accessibilité pour les lecteurs d'écran
        })
    )