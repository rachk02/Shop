# Generated by Django 5.0.2 on 2024-02-23 16:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0013_alter_produit_description_alter_produit_promotion_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creer', models.DateTimeField(auto_now_add=True)),
                ('modifier', models.DateTimeField(auto_now_add=True)),
                ('payer', models.BooleanField(default=False)),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creer'],
            },
        ),
        migrations.CreateModel(
            name='ContenuC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.PositiveIntegerField(default=1)),
                ('prix', models.DecimalField(decimal_places=2, max_digits=10)),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='orders.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='shop.produit')),
            ],
        ),
        migrations.AddIndex(
            model_name='commande',
            index=models.Index(fields=['-creer'], name='orders_comm_creer_931f9c_idx'),
        ),
    ]
