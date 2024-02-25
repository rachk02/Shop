from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from cart.cart import Panier
from .forms import FormulaireDeCC
from .models import CommandeItem
from shop.models import Marque, Categorie

# Create your views here.


marques = Marque.objects.all()
categories = Categorie.objects.all()
m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)


@login_required  # Ajoutez le décorateur ici
def creer_commande(request):
    panier = Panier(request)
    total = panier.get_prix_total()
    if request.method == 'POST':
        formulaire = FormulaireDeCC(request.POST)

        if formulaire.is_valid():
            utilisateur = request.user
            commande = formulaire.save(commit=False)
            commande.utilisateur = utilisateur
            commande.save()

            for item in panier:
                CommandeItem.objects.create(
                    commande=commande,
                    produit=item['produit'],
                    prix=item['prix'],
                    quantite=item['quantite']
                )

            panier.effacer()

            return render(request, 'orders/commande.html', {
                'commande': commande,
                'utilisateur': utilisateur,
                'categories': categories,
                'marques': marques,
                'marques_to_display': marques_to_display,
                'categories_to_display': categories_to_display,
                'total': total
            })

    else:
        formulaire = FormulaireDeCC()

    return render(request, 'orders/cr_commande.html', {
        'panier': panier,
        'formulaire': formulaire,
        'utilisateur': request.user,
        'categories': categories,
        'marques': marques,
        'marques_to_display': marques_to_display,
        'categories_to_display': categories_to_display
    })
