# Generated by Django 5.0.1 on 2024-09-19 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_remove_auction_nft_auction_creator_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='nft_image',
            field=models.FileField(blank=True, null=True, upload_to='nft_images/'),
        ),
    ]
