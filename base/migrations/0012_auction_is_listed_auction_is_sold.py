# Generated by Django 5.0.1 on 2024-09-21 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_ownership'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='is_listed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='auction',
            name='is_sold',
            field=models.BooleanField(default=False),
        ),
    ]
