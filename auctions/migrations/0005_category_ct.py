# Generated by Django 4.2 on 2023-06-12 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_product_category_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='ct',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cts', to='auctions.category'),
        ),
    ]
