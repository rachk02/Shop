from django.db import models
from shop.models import Produit
from account.models import Utilisateur


# Create your models here.


class Commande(models.Model):
    utilisateur = models.ForeignKey(Utilisateur,
                                    on_delete=models.CASCADE)
    creer = models.DateTimeField(auto_now_add=True)
    modifier = models.DateTimeField(auto_now_add=True)
    payer = models.BooleanField(default=False)

    class Meta:
        ordering = ['-creer']
        indexes = [
            models.Index(fields=['-creer']),
        ]

    def __str__(self):
        return f'Commande {self.id} - {self.utilisateur.email}'

    def cout_total(self):
        return sum(item.cout() for item in self.items.all())


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
