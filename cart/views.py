from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Produit, Marque, Categorie
from .cart import Panier
from .forms import FormulaireAjout

# Create your views here.

marques = Marque.objects.all()
categories = Categorie.objects.all()
m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)


@require_POST
def ajouter_produit(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    form = FormulaireAjout(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        panier.ajouter(produit=produit,
                       quantite=cd['quantite'],
                       ecraser_quantite=cd['ecraser'])
    return redirect('cart:panier_detail')


@require_POST
def retirer_produit(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    panier.retirer(produit)
    return redirect('cart:panier_detail')


def panier_detail(request):
    panier = Panier(request)
    for item in panier:
        item['formulaire_maj'] = FormulaireAjout(initial={
            'quantite': item['quantite'],
            'ecraser': True})
    return render(request, 'cart/detail.html', {'panier': panier,
                                                'categories': categories,
                                                'marques': marques,
                                                'marques_to_display': marques_to_display,
                                                'categories_to_display': categories_to_display, })
