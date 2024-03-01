from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, nom, prenom, mdp=None, **extra_fields):
        user = self.model(
            nom=nom,
            prenom=prenom,
            **extra_fields
        )
        user.set_password(mdp)
        user.save(using=self._db)
        return user

    def create_superuser(self, nom, prenom, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(nom, prenom, password, **extra_fields)


class Utilisateur(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=True, null=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=timezone.now)
    date_naissance = models.DateField(null=True, blank=True)
    adresse = models.CharField(max_length=50, null=True, blank=True)
    ville = models.CharField(max_length=50, null=True, blank=True)
    code_postal = models.CharField(max_length=50, null=True, blank=True)
    telephone = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, related_name='utilisateurs', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='utilisateurs', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nom', 'prenom']

    def __str__(self):
        return self.email if self.email else f"{self.nom} {self.prenom}"
