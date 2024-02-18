# Generated by Django 5.0.2 on 2024-02-17 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_alter_produit_options_alter_produit_image_promotion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='description',
            field=models.JSONField(),
        ),
        migrations.AlterField(
            model_name='produit',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.promotion'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='produit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.produit'),
        ),
        migrations.AlterField(
            model_name='promo',
            name='promotion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.promotion'),
        ),
    ]
