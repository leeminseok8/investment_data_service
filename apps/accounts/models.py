from django.db import models

from apps.users.models import User


class Brokerage(models.Model):
    """
    증권사 모델
    """

    brokerage_name = models.CharField("증권사", max_length=20, unique=True)

    class Meta:
        db_table = "brokerages"


class Account(models.Model):
    """
    계좌 정보 모델
    """

    account_name = models.CharField("계좌 이름", max_length=20)
    account_number = models.CharField("계좌 번호", max_length=20, unique=True)
    investment_principal = models.PositiveBigIntegerField("투자 원금", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brokerage = models.ForeignKey(Brokerage, on_delete=models.CASCADE)

    class Meta:
        db_table = "accounts"


class Deposit(models.Model):
    """
    계좌 입금 테이블
    """

    amount = models.PositiveBigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        db_table = "deposits"


class AssetGroup(models.Model):
    """
    자산 그룹 모델
    """

    asset_name = models.CharField("자산 그룹", max_length=16, unique=True)

    class Meta:
        db_table = "assets_groups"


class Stock(models.Model):
    """
    주식 정보 모델
    국제 규격인 ISIN 12자로 제한
    """

    stock_name = models.CharField("종목명", max_length=30)
    ISIN = models.CharField("ISIN", max_length=12, unique=True)
    current_price = models.PositiveIntegerField("현재가", default=0, null=True)
    group = models.ForeignKey(AssetGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = "stocks"


class Asset(models.Model):
    """
    현재 계좌의 주식 수량 모델
    """

    quantity = models.PositiveIntegerField("수량", default=0)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)

    class Meta:
        db_table = "assets"
