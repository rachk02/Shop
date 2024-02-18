from django.contrib import admin
from .models import Marque, Categorie, Produit, Promotion, Promo


# Register your models here.

@admin.register(Marque)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Categorie)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Produit)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'prix', 'disponible', 'ajouter', 'modifier']
    list_filter = ['disponible', 'ajouter', 'modifier']
    list_editable = ['prix', 'disponible']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'slug', 'ajouter', 'modifier']
    list_filter = ['ajouter', 'modifier']
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ['produit', 'promotion']
    list_filter = ['date_debut', 'date_fin']
