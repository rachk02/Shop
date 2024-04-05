from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from cart.cart import Panier
from django.template.loader import render_to_string
from .forms import FormulaireDeCC
from .models import CommandeItem
from django.conf import settings
from django.http import HttpResponse
from shop.models import Marque, Categorie
from .models import Commande, CommandeItem
from .forms import FormulaireDeCC
from .tasks import commande_passer
from django.urls import reverse
import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from shop.forms import FormulaireRA

# Create your views here.


marques = Marque.objects.all()
categories = Categorie.objects.all()
m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)
formulaire_recherche = FormulaireRA()


@login_required
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

            commande_passer.delay(commande.id)

            request.session['id_commande'] = commande.id

            return redirect(reverse('payment:processus_de_paiement'))

    else:
        formulaire = FormulaireDeCC()

    return render(request, 'orders/cr_commande.html', {
        'panier': panier,
        'formulaire': formulaire,
        'utilisateur': request.user,
        'categories': categories,
        'marques': marques,
        'marques_to_display': marques_to_display,
        'categories_to_display': categories_to_display,
        'formulaire': formulaire_recherche,
    })


@staff_member_required
def admin_commande_pdf(request, id_commande):
    commande = get_object_or_404(Commande, id=id_commande)
    html = render_to_string('orders/pdf.html',
                            {'commande': commande})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=commande_{commande.generer_numero_commande()}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT / 'bootstrap/css/bootstrap.min.css')])
    return response


@login_required
def commande_pdf(request, id_commande):
    commande = get_object_or_404(Commande, id=id_commande)

    if commande.utilisateur != request.user:
        return HttpResponse("Unauthorized", status=401)

    html = render_to_string('orders/pdf.html', {'commande': commande})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=commande_{commande.generer_numero_commande()}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
                                           stylesheets=[weasyprint.CSS(
                                               settings.STATIC_ROOT / 'bootstrap/css/bootstrap.min.css')])
    return response


@login_required
def liste_commandes(request):
    user = request.user
    status = request.GET.get('status', '')

    commandes = Commande.objects.filter(utilisateur=user)
    if status == 'paid':
        commandes = commandes.filter(payer=True)
    elif status == 'not-paid':
        commandes = commandes.filter(payer=False)

    return render(request, 'orders/liste_commandes.html', {
        'commandes': commandes,
        'categories': categories,
        'marques': marques,
        'marques_to_display': marques_to_display,
        'categories_to_display': categories_to_display,
        'formulaire': formulaire_recherche,
    })


def commande_detail(request, id):
    commande = get_object_or_404(Commande, id=id)
    return render(request, 'orders/commande_detail.html', {'commande': commande,
                                                           'utilisateur': request.user,
                                                           'categories': categories,
                                                            'marques': marques,
                                                            'marques_to_display': marques_to_display,
                                                            'categories_to_display': categories_to_display,
                                                            'formulaire': formulaire_recherche,
                                                           })
