from django.shortcuts import render, redirect, reverse, get_object_or_404
import stripe
from django.conf import settings
from orders.models import Commande
from decimal import Decimal
from shop.models import Marque, Categorie
import logging
from shop.forms import FormulaireRA

# Create your views here.


logger = logging.getLogger(__name__)
marques = Marque.objects.all()
categories = Categorie.objects.all()
m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)
formulaire_recherche = FormulaireRA()


def paiement_unique(request, id_commande):
    commande = get_object_or_404(Commande, id=id_commande)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.api_version = settings.STRIPE_API_VERSION
    stripe.api_base = "https://api.stripe.com"
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:paiement_reussi'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:paiement_annuler'))
        # Stripe checkout session data
        session_data = {
            'payment_method_types': ['card'],
            'mode': 'payment',
            'client_reference_id': commande.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # add order items to the Stripe checkout session
        for item in commande.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.prix * Decimal('100')),
                    'currency': 'XOF',
                    'product_data': {
                        'name': item.produit.nom,
                    },
                },
                'quantity': item.quantite,
            })

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, 'payment/processus.html', {
            'commande': commande,
            'utilisateur': request.user,
            'categories': categories,
            'marques': marques,
            'marques_to_display': marques_to_display,
            'categories_to_display': categories_to_display,
            'formulaire': formulaire_recherche,
        })


def processus_de_paiement(request):
    id_commande = request.session.get('id_commande', None)
    commande = get_object_or_404(Commande, id=id_commande)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.api_version = settings.STRIPE_API_VERSION
    stripe.api_base = "https://api.stripe.com"
    if request.method == 'POST':
        success_url = request.build_absolute_uri(
            reverse('payment:paiement_reussi'))
        cancel_url = request.build_absolute_uri(
            reverse('payment:paiement_annuler'))
        # Stripe checkout session data
        session_data = {
            'payment_method_types': ['card'],
            'mode': 'payment',
            'client_reference_id': commande.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': []
        }

        # add order items to the Stripe checkout session
        for item in commande.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.prix),
                    'currency': 'XOF',
                    'product_data': {
                        'name': item.produit.nom,
                    },
                },
                'quantity': item.quantite,
            })

        # create Stripe checkout session
        session = stripe.checkout.Session.create(**session_data)

        # redirect to Stripe payment form
        return redirect(session.url, code=303)

    else:
        return render(request, 'payment/processus.html', {
            'commande': commande,
            'utilisateur': request.user,
            'categories': categories,
            'marques': marques,
            'marques_to_display': marques_to_display,
            'categories_to_display': categories_to_display,
            'formulaire': formulaire_recherche,
        })


def paiement_reussi(request):
    return render(request, 'payment/reussi.html', {
        'categories': categories,
        'marques': marques,
        'marques_to_display': marques_to_display,
        'categories_to_display': categories_to_display,
        'utilisateur': request.user,
        'formulaire': formulaire_recherche,
    })


def paiement_annuler(request):
    return render(request, 'payment/annuler.html', {
        'categories': categories,
        'marques': marques,
        'marques_to_display': marques_to_display,
        'categories_to_display': categories_to_display,
        'utilisateur': request.user,
        'formulaire': formulaire_recherche,
    })
