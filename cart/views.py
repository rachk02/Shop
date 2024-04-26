from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Produit, Marque, Categorie
from .cart import Panier
from .forms import FormulaireAjout, FormulaireMajQuantite, FormulaireSimple
from shop.forms import FormulaireRA

# Create your views here.

marques = Marque.objects.all()
categories = Categorie.objects.all()
m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)
formulaire_recherche = FormulaireRA()


@require_POST
def ajouter_produit(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    formulaire = FormulaireAjout(request.POST)
    if formulaire.is_valid():
        cd = formulaire.cleaned_data
        panier.ajouter(produit=produit,
                       quantite=cd['quantite'])
    return redirect('cart:panier_detail')


@require_POST
def ajouter_produit_direct(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    formulaire = FormulaireSimple(request.POST)
    if formulaire.is_valid():
        panier.ajouter_produit_par_id(produit=produit)
    return redirect('cart:panier_detail')


@require_POST
def maj_quantite(request, id_produit):
    panier = Panier(request)
    produit = get_object_or_404(Produit, id=id_produit)
    if request.method == 'POST':
        formulaire = FormulaireMajQuantite(request.POST)
        if formulaire.is_valid():
            cd = formulaire.cleaned_data
            panier.maj(produit=produit,
                       quantite=cd['quantite'])
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
            'quantite': item['quantite']})
    return render(request, 'cart/detail.html', {'panier': panier,
                                                'categories': categories,
                                                'marques': marques,
                                                'marques_to_display': marques_to_display,
                                                'categories_to_display': categories_to_display,
                                                'utilisateur': request.user,
                                                'formulaire_recherche': formulaire_recherche,
                                                })
