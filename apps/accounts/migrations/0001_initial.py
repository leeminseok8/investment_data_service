# Generated by Django 4.1.1 on 2022-09-21 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Brokerage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("brokerage_name", models.CharField(max_length=20, verbose_name="증권사")),
            ],
            options={
                "db_table": "brokerages",
            },
        ),
        # migrations.CreateModel(
        #     name="User",
        #     fields=[
        #         (
        #             "id",
        #             models.BigAutoField(
        #                 auto_created=True,
        #                 primary_key=True,
        #                 serialize=False,
        #                 verbose_name="ID",
        #             ),
        #         ),
        #         ("user_name", models.CharField(max_length=16, verbose_name="유저 이름")),
        #     ],
        #     options={
        #         "db_table": "users",
        #     },
        # ),
        migrations.CreateModel(
            name="UserBrokerage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "brokerage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.brokerage",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.user"
                    ),
                ),
            ],
            options={
                "db_table": "users_brokerages",
            },
        ),
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account_name", models.CharField(max_length=20, verbose_name="계좌 이름")),
                (
                    "account_number",
                    models.CharField(max_length=20, verbose_name="계좌 번호"),
                ),
                (
                    "investment_principal",
                    models.PositiveBigIntegerField(default=0, verbose_name="투자 원금"),
                ),
                (
                    "users_brokerages",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.userbrokerage",
                    ),
                ),
            ],
            options={
                "db_table": "accounts",
            },
        ),
    ]
