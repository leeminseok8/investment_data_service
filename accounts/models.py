from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(AbstractBaseUser):
    user_name = models.CharField("유저 이름", max_length=16, unique=True)

    USERNAME_FIELD = "user_name"

    class Meta:
        db_table = "users"


class Brokerage(models.Model):
    brokerage_name = models.CharField("증권사", max_length=20, unique=True)

    class Meta:
        db_table = "brokerages"


class Account(models.Model):
    account_name = models.CharField("계좌 이름", max_length=20)
    account_number = models.CharField("계좌 번호", max_length=20, unique=True)
    investment_principal = models.PositiveBigIntegerField("투자 원금", default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brokerage = models.ForeignKey(Brokerage, on_delete=models.CASCADE)

    class Meta:
        db_table = "accounts"
