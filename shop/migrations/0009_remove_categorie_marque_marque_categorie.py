# Generated by Django 5.0.2 on 2024-02-14 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_categorie_marque'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorie',
            name='marque',
        ),
        migrations.AddField(
            model_name='marque',
            name='categorie',
            field=models.ManyToManyField(through='shop.Produit', to='shop.categorie'),
        ),
    ]