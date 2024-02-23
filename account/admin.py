from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import Utilisateur


# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = Utilisateur
    list_display = ('email', 'nom', 'prenom', 'date_naissance', 'is_active', 'is_staff')
    search_fields = ('email', 'nom', 'prenom', 'date_naissance')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informations personnelles', {'fields': ('nom', 'prenom', 'date_naissance', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nom', 'prenom', 'date_naissance', 'image', 'password1', 'password2'),
        }),
    )


admin.site.register(Utilisateur, CustomUserAdmin)
