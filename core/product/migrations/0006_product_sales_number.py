# Generated by Django 4.2.3 on 2023-09-08 10:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0005_wishlist"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sales_number",
            field=models.IntegerField(default=0),
        ),
    ]