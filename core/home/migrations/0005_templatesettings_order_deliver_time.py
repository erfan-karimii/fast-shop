# Generated by Django 4.2.3 on 2023-08-30 12:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0004_templatesettings_copyright_text_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="templatesettings",
            name="order_deliver_time",
            field=models.CharField(
                default=" از انبار مَسای کالا طی 2 روز کاری",
                max_length=450,
                verbose_name="زمان ارسال محصول ",
            ),
        ),
    ]
