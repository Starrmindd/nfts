# Generated by Django 5.0.1 on 2024-09-21 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_auction_is_listed_auction_is_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='admin_list',
            field=models.BooleanField(default=False),
        ),
    ]
