import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "investment.settings")
django.setup()

from accounts.models import User, Brokerage, UserBrokerage, Account
from stocks.models import Stock, Asset

ACCOUNT_PATH = "./resource/account_info_set.csv"
STOCK_ASSET_PATH = "./resource/stock_asset_info_set.csv"
USER_BROKERAGE_PATH = "./resource/user_brokerage_info_set.csv"


def insert_user():
    with open(USER_BROKERAGE_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            user_name = row[0]

            User.objects.create(
                user_name=user_name,
            )

    print("SECCESSED UPLOAD USER DATA!")


def insert_brokerage():
    with open(USER_BROKERAGE_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            brokerage_name = row[1]

            Brokerage.objects.create(
                brokerage_name=brokerage_name,
            )

    print("SECCESSED UPLOAD BROKERAGE DATA!")


def insert_user_brokerage():
    with open(USER_BROKERAGE_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            user_id = row[2]
            brokerage_id = row[3]
            user = User.objects.get(id=user_id)
            brokerage = Brokerage.objects.get(id=brokerage_id)

            UserBrokerage.objects.create(user=user, brokerage=brokerage)

    print("SECCESSED UPLOAD USER_BROKERAGE DATA!")


def insert_account():
    with open(ACCOUNT_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            account_name = row[0]
            account_number = row[1]
            investment_principal = row[2]
            users_brokerages_id = row[3]
            users_brokerages = UserBrokerage.objects.get(id=users_brokerages_id)

            Account.objects.create(
                account_name=account_name,
                account_number=account_number,
                investment_principal=investment_principal,
                users_brokerages=users_brokerages,
            )

    print("SECCESSED UPLOAD ACCOUNT DATA!")


def insert_stock():
    with open(STOCK_ASSET_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            stock_name = row[0]
            ISIN = row[1]
            asset_name = row[2]

            Stock.objects.create(
                stock_name=stock_name, ISIN=ISIN, asset_name=asset_name
            )

    print("SECCESSED UPLOAD STOCK DATA!")


def insert_asset():
    with open(STOCK_ASSET_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            current_price = row[4]
            quantity = row[5]
            account_id = row[6]
            stock_id = row[7]
            account = Account.objects.get(id=account_id)
            stock = Stock.objects.get(id=stock_id)

            Asset.objects.create(
                current_price=current_price,
                quantity=quantity,
                account=account,
                stock=stock,
            )

    print("SECCESSED UPLOAD ASSET DATA!")


insert_user()
insert_brokerage()
insert_user_brokerage()
insert_account()
insert_stock()
insert_asset()
