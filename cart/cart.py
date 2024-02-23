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
        self.utilisateur = request.user if request.user.is_authenticated else None

    def __iter__(self):
        id_produits = self.panier.keys()
        produits = Produit.objects.filter(id__in=id_produits)
        panier = self.panier.copy()

        for produit in produits:
            produit_id_str = str(produit.id)
            panier_item = panier.get(produit_id_str, {})
            panier_item['produit'] = produit
            panier_item['prix'] = Decimal(panier_item.get('prix', 0))
            panier_item['prix_total'] = panier_item['prix'] * panier_item.get('quantite', 0)
            yield panier_item

    def __len__(self):
        return sum(item['quantite'] for item in self.panier.values())

    def ajouter(self, produit, quantite=1):
        id_produit = str(produit.id)

        def is_promote(produit):
            if produit.promotion:
                prix = produit.prix_promotionnel()
            else:
                prix = produit.prix
            return prix

        prix = is_promote(produit)

        if id_produit not in self.panier:
            self.panier[id_produit] = {'quantite': quantite,
                                       'prix': str(prix)}
        else:
            self.panier[id_produit]['quantite'] += quantite
            self.panier[id_produit]['prix'] = str(prix)

        if self.utilisateur:
            self.panier[id_produit]['utilisateur'] = self.utilisateur.id

        self.sauvegarder()

    def maj(self, produit, quantite=1):
        id_produit = str(produit.id)

        def is_promote(produit):
            if produit.promotion:
                prix = produit.prix_promotionnel()
            else:
                prix = produit.prix
            return prix

        prix = is_promote(produit)

        if id_produit not in self.panier:
            self.panier[id_produit] = {'quantite': quantite,
                                       'prix': str(prix)}
        else:
            self.panier[id_produit]['quantite'] = quantite
            self.panier[id_produit]['prix'] = str(prix)

        if self.utilisateur:
            self.panier[id_produit]['utilisateur'] = self.utilisateur.id

        self.sauvegarder()

    def ajouter_produit_par_id(self, produit):
        id_produit = str(produit.id)

        def is_promote(produit):
            if produit.promotion:
                prix = produit.prix_promotionnel()
            else:
                prix = produit.prix
            return prix

        prix = is_promote(produit)

        quantite = 1

        if id_produit not in self.panier:
            self.panier[id_produit] = {'quantite': quantite,
                                       'prix': str(prix)}
        else:
            self.panier[id_produit]['quantite'] += quantite
            self.panier[id_produit]['prix'] = str(prix)
        if self.utilisateur:
            self.panier[id_produit]['utilisateur'] = self.utilisateur.id

        self.sauvegarder()

    def sauvegarder(self):
        self.session.modified = True

    def retirer(self, produit):
        id_produit = str(produit.id)
        if id_produit in self.panier:
            del self.panier[id_produit]
            self.sauvegarder()

    def get_prix_total(self):
        return sum(Decimal(item['prix']) * item['quantite'] for item in self.panier.values())

    def effacer(self):
        del self.session[settings.CART_SESSION_ID]
        self.sauvegarder()
