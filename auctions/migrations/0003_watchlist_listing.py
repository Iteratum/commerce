# Generated by Django 4.2 on 2023-06-10 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='listing',
            field=models.ManyToManyField(null=True, related_name='watchlist_item', to='auctions.listing'),
        ),
    ]
