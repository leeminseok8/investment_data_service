# Generated by Django 4.1.1 on 2022-09-22 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stocks", "0002_assetgroup_remove_asset_current_price_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stock",
            name="current_price",
            field=models.PositiveIntegerField(default=0, null=True, verbose_name="현재가"),
        ),
    ]
