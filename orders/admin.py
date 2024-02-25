from django.contrib import admin
from .models import Commande, CommandeItem


# Register your models here.


class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    raw_id_fields = ['produit']


class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prenom', 'creer', 'modifier', 'payer']
    list_filter = ['payer', 'creer', 'modifier']
    inlines = [CommandeItemInline]


class CommandeItemAdmin(admin.ModelAdmin):
    list_display = ['commande', 'produit', 'quantite', 'prix']
    list_filter = ['commande__payer', 'produit']


admin.site.register(Commande, CommandeAdmin)
admin.site.register(CommandeItem, CommandeItemAdmin)
