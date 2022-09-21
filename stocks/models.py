from django.db import models

from ..accounts.models import Account


class Stock(models.Model):
    stock_name = models.CharField("종목명", max_length=30)
    ISIN = models.CharField("ISIN", max_length=12)
    asset_name = models.CharField("자산 그룹", max_length=16)

    class Meta:
        db_table = "stocks"


class Asset(models.Model):
    current_price = models.PositiveIntegerField("현재가")
    quantity = models.PositiveIntegerField("수량", default=0)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        db_table = "assets"
