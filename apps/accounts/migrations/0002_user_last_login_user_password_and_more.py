# Generated by Django 4.1.1 on 2022-09-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        # migrations.AddField(
        #     model_name='user',
        #     name='last_login',
        #     field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        # ),
        # migrations.AddField(
        #     model_name='user',
        #     name='password',
        #     field=models.CharField(default=True, max_length=128, verbose_name='password'),
        #     preserve_default=False,
        # ),
        migrations.AlterField(
            model_name="account",
            name="account_number",
            field=models.CharField(max_length=20, unique=True, verbose_name="계좌 번호"),
        ),
        migrations.AlterField(
            model_name="brokerage",
            name="brokerage_name",
            field=models.CharField(max_length=20, unique=True, verbose_name="증권사"),
        ),
        # migrations.AlterField(
        #     model_name="user",
        #     name="user_name",
        #     field=models.CharField(max_length=16, unique=True, verbose_name="유저 이름"),
        # ),
    ]
