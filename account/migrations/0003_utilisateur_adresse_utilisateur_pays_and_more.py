# Generated by Django 5.0.2 on 2024-02-22 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_utilisateur_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='adresse',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='pays',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='telephone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='utilisateur',
            name='ville',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
