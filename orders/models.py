from django.db import models
from shop.models import Produit
from account.models import Utilisateur
from django.conf import settings


# Create your models here.


class Commande(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    creer = models.DateTimeField(auto_now_add=True)
    modifier = models.DateTimeField(auto_now_add=True)
    payer = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)

    def nom(self):
        return f'{self.utilisateur.nom}'

    def prenom(self):
        return f'{self.utilisateur.prenom}'

    def email(self):
        return f'{self.utilisateur.email}'

    def adresse(self):
        return f'{self.utilisateur.adresse}'

    def code_postal(self):
        return f'{self.utilisateur.code_postal}'

    def ville(self):
        return f'{self.utilisateur.ville}'

    def telephone(self):
        return f'{self.utilisateur.telephone}'

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        if '_test_' in settings.STRIPE_SECRET_KEY:

            path = '/test/'
        else:

            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'

    def generer_numero_commande(self):
        partie_fixe = hex(self.id)[2:].zfill(4)

        date_partie_variable = self.creer.strftime('%Y%m%d') if self.creer else '00000000'

        if self.utilisateur:
            prenom_partie_variable = self.utilisateur.prenom[0].upper()
            nom_partie_variable = self.utilisateur.nom[-1].upper()
        else:
            prenom_partie_variable = 'X'
            nom_partie_variable = 'X'

        numero_commande_masque = f'CMD-{partie_fixe}-{date_partie_variable}-{prenom_partie_variable}{nom_partie_variable}'

        return numero_commande_masque

    class Meta:
        ordering = ['-creer']
        indexes = [models.Index(fields=['-creer'])]

    def __str__(self):
        return f'{self.generer_numero_commande()}'

    def cout_total(self):
        total = f"{sum(item.cout() for item in self.items.all()):,.2f}"
        return float(total.replace(',', ''))

    def frais(self):
        x = 0.01
        frais = f"{self.cout_total() * x:,.2f}"
        return float(frais.replace(',', ''))



class CommandeItem(models.Model):
    commande = models.ForeignKey(Commande,
                                 related_name='items', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit,
                                related_name='order_items', on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    prix = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantite} x {self.produit.nom}'

    def cout(self):
        return self.quantite * self.prix

    def ct(self):
        return self.quantite * self.prix
