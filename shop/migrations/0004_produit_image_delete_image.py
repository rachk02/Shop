# Generated by Django 5.0.2 on 2024-02-12 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_remove_produit_images_image_produit'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='produit_images/'),
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]