from django.db import models


class User(models.Model):
    user_name = models.CharField("유저 이름", max_length=16)

    class Meta:
        db_table = "users"


class Brokerage(models.Model):
    brokerage_name = models.CharField("증권사", max_length=20)

    class Meta:
        db_table = "brokerages"


class UserBrokerage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brokerage = models.ForeignKey(Brokerage, on_delete=models.CASCADE)

    class Meta:
        db_table = "users_brokerages"


class Account(models.Model):
    account_name = models.CharField("계좌 이름", max_length=20)
    account_number = models.CharField("계좌 번호", max_length=20)
    investment_principal = models.PositiveBigIntegerField("투자 원금", default=0)
    users_brokerages = models.ForeignKey(UserBrokerage, on_delete=models.CASCADE)

    class Meta:
        db_table = "accounts"
