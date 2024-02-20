from decimal import Decimal
from django.conf import settings
from shop.models import Produit


class Panier:
    def __init__(self, request):
        self.session = request.session
        panier = self.session.get(settings.CART_SESSION_ID)
        if not panier:
            panier = self.session[settings.CART_SESSION_ID] = {}
        self.panier = panier

    def __iter__(self):
        id_produits = self.panier.keys()
        produits = Produit.objects.filter(id__in=id_produits)
        panier = self.panier.copy()
        for produit in produits:
            panier[str(produit.id)]['produit'] = produit
        for item in panier.values():
            item['prix'] = Decimal(item['prix'])
            item['prix_total'] = item['prix'] * item['quantite']
            yield item

    def __len__(self):
        return sum(item['quantite'] for item in self.panier.values())

    def ajouter(self, produit, quantite=1, ecraser_quantite=False):
        id_produit = str(produit.id)
        def is_promote(produit):
            if produit.promotion:
                prix = produit.prix_promotionnel()
            else:
                prix = produit.prix
            return prix
        prix = is_promote(produit)
        if id_produit not in self.panier:
            self.panier[id_produit] = {'quantite': 0,
                                       'prix': str(prix)}
        if ecraser_quantite:
            self.panier[id_produit]['quantite'] = quantite
        else:
            self.panier[id_produit]['quantite'] += quantite
        self.sauvegarder()

    def sauvegarder(self):
        self.session.modified = True

    def retirer(self, produit):
        id_produit = str(produit.id)
        if id_produit in self.panier:
            del self.panier[id_produit]
            self.sauvegarder()

    def get_prix_total(self):
        return sum(Decimal(item['prix']) * item['quantite'] for item in self.
                   panier.values())

    def effacer(self):
        del self.session[settings.CART_SESSION_ID]
        self.sauvegarder()
