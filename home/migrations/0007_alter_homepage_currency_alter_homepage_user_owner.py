# Generated by Django 4.0.5 on 2022-06-22 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_homepage_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='currency',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='user_owner',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]