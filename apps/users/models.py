from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class User(
    AbstractBaseUser,
):
    """
    유저 모델
    인증 절차를 위해 유저 모델로 생성
    """

    user_name = models.CharField("유저 이름", max_length=16, unique=True)

    USERNAME_FIELD = "user_name"

    class Meta:
        db_table = "users"
