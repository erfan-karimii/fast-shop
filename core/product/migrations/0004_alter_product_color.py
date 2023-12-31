# Generated by Django 4.2.3 on 2023-08-31 13:51

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0003_product_color"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="color",
            field=colorfield.fields.ColorField(
                blank=True,
                default=None,
                image_field=None,
                max_length=18,
                null=True,
                samples=[
                    ("#FFFFFF", "white"),
                    ("#000000", "black"),
                    ("#0000ff", "blue"),
                    ("#ffd800", "yellow"),
                    ("#ff0000", "red"),
                ],
            ),
        ),
    ]
