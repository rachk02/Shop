from django.shortcuts import render, get_object_or_404
from .models import Marque, Categorie, Produit, Promo
import random
from cart.forms import FormulaireAjout

m_slug_to_display = ['apple', 'samsung', 'asus', 'dell', 'sony']
marques_to_display = Marque.objects.filter(slug__in=m_slug_to_display)
c_slug_to_display = ['ordinateurs', 'smartphones', 'tablettes', 'gaming', 'cinema']
categories_to_display = Categorie.objects.filter(slug__in=c_slug_to_display)
formulaire_ajout = FormulaireAjout()


def promo_clearer():
    promos = Promo.objects.all()
    for promo in promos:
        if not promo.is_active():
            promo.promotion.delete()
            promo.delete()


def homepage(request):
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    promo_clearer()
    produits = Produit.objects.filter(disponible=True)
    produits_aleatoires = random.sample(list(produits), 12)
    marques_aleatoires = random.sample(list(marques), 9)
    return render(request,
                  'shop/index.html',
                  {'marques': marques,
                   'categories': categories,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'produits': produits_aleatoires,
                   'marques_aleatoires': marques_aleatoires,
                   'formulaire_ajout': formulaire_ajout,
                   'utilisateur': request.user})


def marque_list(request):
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    return render(request,
                  'shop/marque/marque_list.html',
                  {'marques': marques,
                   'categories': categories,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user})


def categorie_list(request):
    categories = Categorie.objects.all()
    marques = Marque.objects.all()
    return render(request,
                  'shop/categorie/categorie_list.html',
                  {'categories': categories,
                   'marques': marques,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'utilisateur': request.user})


def produit_list(request, categorie_slug=None, marque_slug=None):
    categorie = None
    marque = None
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    promo_clearer()
    produits = Produit.objects.filter(disponible=True)
    if marque_slug and not categorie_slug:
        marque = get_object_or_404(Marque,
                                   slug=marque_slug)
        multi_categories = marque.categorie.all()
        produits = produits.filter(categorie__in=multi_categories,
                                   disponible=True)
    elif categorie_slug and not marque_slug:
        categorie = get_object_or_404(Categorie,
                                      slug=categorie_slug)
        produits = produits.filter(categorie=categorie)
    elif marque_slug and categorie_slug:
        marque = get_object_or_404(Marque,
                                   slug=marque_slug)
        multi_categories = marque.categorie.all()
        produits = produits.filter(categorie=categorie,
                                   categorie__in=multi_categories,
                                   disponible=True)
    return render(request,
                  'shop/produit/list.html',
                  {'categorie': categorie,
                   'categories': categories,
                   'marque': marque,
                   'marques': marques,
                   'produits': produits,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'formulaire_ajout': formulaire_ajout,
                   'utilisateur': request.user})


def produit_list_marque(request, marque_slug):
    marque = get_object_or_404(Marque, slug=marque_slug)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    promo_clearer()
    produits = Produit.objects.filter(marque=marque, disponible=True)

    for produit in produits:
        promo = Promo.objects.filter(produit=produit).first()
        if promo and promo.is_active():
            produit.promotion = promo.promotion

    return render(request,
                  'shop/produit/list.html',
                  {'marque': marque,
                   'categories': categories,
                   'marques': marques,
                   'produits': produits,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'formulaire_ajout': formulaire_ajout,
                   'utilisateur': request.user})


def produit_list_categorie(request, categorie_slug):
    categorie = get_object_or_404(Categorie, slug=categorie_slug)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    promo_clearer()
    produits = Produit.objects.filter(categorie=categorie, disponible=True)

    for produit in produits:
        promo = Promo.objects.filter(produit=produit).first()
        if promo and promo.is_active():
            produit.promotion = promo.promotion

    return render(request,
                  'shop/produit/list.html',
                  {'categorie': categorie,
                   'categories': categories,
                   'marques': marques,
                   'produits': produits,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'formulaire_ajout': formulaire_ajout,
                   'utilisateur': request.user})


def produit_list_marque_categorie(request, marque_slug, categorie_slug):
    marque = get_object_or_404(Marque, slug=marque_slug)
    categorie = get_object_or_404(Categorie, slug=categorie_slug)
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    promo_clearer()
    produits = Produit.objects.filter(marque=marque, categorie=categorie, disponible=True)

    for produit in produits:
        promo = Promo.objects.filter(produit=produit).first()
        if promo and promo.is_active():
            produit.promotion = promo.promotion

    return render(request,
                  'shop/produit/list.html',
                  {'marque': marque,
                   'categorie': categorie,
                   'categories': categories,
                   'marques': marques,
                   'produits': produits,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'formulaire_ajout': formulaire_ajout,
                   'utilisateur': request.user})


def produit_detail(request, id, slug):
    marques = Marque.objects.all()
    categories = Categorie.objects.all()
    produit = get_object_or_404(Produit,
                                id=id,
                                slug=slug,
                                disponible=True)
    return render(request,
                  'shop/produit/detail.html',
                  {'produit': produit,
                   'marques': marques,
                   'categories': categories,
                   'marques_to_display': marques_to_display,
                   'categories_to_display': categories_to_display,
                   'formulaire_ajout': formulaire_ajout,
                   'utilisateur': request.user})
