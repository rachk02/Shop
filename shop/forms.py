from django import forms


class FormulaireRA(forms.Form):
    mot_cle = forms.CharField(
        label='recherche',
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'recherche',
            'style': 'height: 100%; max-width: 100%; border: none; background-color: white;',
        })
    )