from django import forms


class FormulaireAjout(forms.Form):
    quantite = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=99,
        widget=forms.NumberInput(attrs={'class': 'ref-quantity-input'})
    )
    ecraser = forms.BooleanField(required=False,
                                 initial=False,
                                 widget=forms.HiddenInput)
