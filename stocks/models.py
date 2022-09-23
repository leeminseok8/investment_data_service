from django.db import models

from accounts.models import Account


class AssetGroup(models.Model):
    asset_name = models.CharField("자산 그룹", max_length=16, unique=True)

    class Meta:
        db_table = "assets_groups"


class Stock(models.Model):
    stock_name = models.CharField("종목명", max_length=30)
    ISIN = models.CharField("ISIN", max_length=12, unique=True)
    current_price = models.PositiveIntegerField("현재가", default=0, null=True)
    group = models.ForeignKey(AssetGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = "stocks"


class Asset(models.Model):
    quantity = models.PositiveIntegerField("수량", default=0)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        db_table = "assets"
