from django.contrib import admin
from .models import Commande, CommandeItem
from django.utils.safestring import mark_safe
from django.urls import reverse


# Register your models here.

class CommandeItemInline(admin.TabularInline):
    model = CommandeItem
    raw_id_fields = ['produit']


class CommandeAdmin(admin.ModelAdmin):
    list_display = ['id', 'nom', 'prenom', 'email', 'telephone', 'adresse', 'code_postal', 'ville', 'payer',
                    'ref_paiement', 'commande_pdf', 'creer', 'modifier']
    list_filter = ['payer', 'creer', 'modifier']
    inlines = [CommandeItemInline]

    def ref_paiement(self, obj):
        url = obj.get_stripe_url()
        if obj.stripe_id:
            html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
            return mark_safe(html)
        return ''

    ref_paiement.short_description = 'Stripe'

    def commande_pdf(self, obj):
        url = reverse('orders:admin_commande_pdf', args=[obj.id])
        return mark_safe(f'<a href="{url}">PDF</a>')

    commande_pdf.short_description = 'Facture'


class CommandeItemAdmin(admin.ModelAdmin):
    list_display = ['commande', 'produit', 'quantite', 'prix']
    list_filter = ['commande__payer', 'produit']


admin.site.register(Commande, CommandeAdmin)
admin.site.register(CommandeItem, CommandeItemAdmin)
