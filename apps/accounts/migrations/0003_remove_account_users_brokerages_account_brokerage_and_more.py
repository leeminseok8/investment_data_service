# Generated by Django 4.1.1 on 2022-09-23 05:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_last_login_user_password_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="users_brokerages",
        ),
        migrations.AddField(
            model_name="account",
            name="brokerage",
            field=models.ForeignKey(
                default=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.brokerage",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="account",
            name="user",
            field=models.ForeignKey(
                default=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.user",
            ),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name="UserBrokerage",
        ),
    ]
