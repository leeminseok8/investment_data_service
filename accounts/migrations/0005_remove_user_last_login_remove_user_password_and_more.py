# Generated by Django 4.1.1 on 2022-09-26 14:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_deposit"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="last_login",
        ),
        migrations.RemoveField(
            model_name="user",
            name="password",
        ),
        migrations.AlterField(
            model_name="account",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
            ),
        ),
        migrations.AlterField(
            model_name="deposit",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="accounts.user"
            ),
        ),
    ]