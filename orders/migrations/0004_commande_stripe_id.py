# Generated by Django 5.0.2 on 2024-02-29 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_rename_commandeitems_commandeitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
