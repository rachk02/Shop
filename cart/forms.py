from django import forms


class FormulaireAjout(forms.Form):
    quantite = forms.IntegerField(
        initial=1,
        min_value=1,
        max_value=99,
        widget=forms.NumberInput(attrs={'class': 'ref-quantity-input'})
    )


class FormulaireSimple(forms.Form):
    def vide(self):
        return None


class FormulaireMajQuantite(forms.Form):
    quantite = forms.IntegerField(min_value=1,
                                  widget=forms.HiddenInput())
