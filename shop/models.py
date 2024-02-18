from django.utils import timezone
from django.db import models
from django.urls import reverse


class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    image = models.ImageField(upload_to='images/categories/%Y/%m/%d', blank=True, null=True)

    class Meta:
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
        ]
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('shop:produit_list_categorie',
                       args=[self.slug])


class Marque(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, null=True)
    categorie = models.ManyToManyField(Categorie, through="Produit")
    image = models.ImageField(upload_to='images/marques/%Y/%m/%d', blank=True, null=True)

    class Meta:
        ordering = ['nom']
        indexes = [
            models.Index(fields=['nom']),
        ]
        verbose_name = 'marque'
        verbose_name_plural = 'marques'

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('shop:produit_list_marque',
                       args=[self.slug])


class Promotion(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, null=True)
    taux_de_reduction = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    ajouter = models.DateTimeField(default=timezone.now)
    modifier = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['modifier']
        indexes = [
            models.Index(fields=['nom']),
        ]

    def __str__(self):
        return self.nom


class Produit(models.Model):
    nom = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, null=True)
    description = models.JSONField()
    disponible = models.BooleanField(default=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE)
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='images/produits/%Y/%m/%d/', null=True)
    ajouter = models.DateTimeField(default=timezone.now)
    modifier = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['modifier']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['nom']),
            models.Index(fields=['-ajouter']),
        ]

    def __str__(self):
        return self.nom

    def get_absolute_url(self):
        return reverse('shop:produit_detail',
                       args=[self.id, self.slug])

    def prix_promotionnel(self):
        prix_reduit = self.prix * (1 - self.promotion.taux_de_reduction / 100)
        self.prix = prix_reduit
        return self.prix

    def is_active(self):
        return self.ajouter <= timezone.now() <= self.modifier


class Promo(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.SET_NULL, null=True, blank=True)
    produit = models.ForeignKey(Produit, on_delete=models.SET_NULL, null=True, blank=True)
    date_debut = models.DateTimeField(null=True)
    date_fin = models.DateTimeField(null=True)

    class Meta:
        ordering = ['date_fin']

    def __str__(self):
        return f"{self.promotion} - {self.produit}"

    def is_active(self):
        return self.date_debut <= timezone.now() <= self.date_fin if self.date_debut and self.date_fin else False
