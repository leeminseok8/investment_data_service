import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "investment.settings")
django.setup()

from apps.accounts.models import User, Brokerage, Account, AssetGroup, Stock, Asset

USER_PATH = "./resource/user_info_set.csv"
STOCK_PATH = "./resource/stock_info_set.csv"
ASSET_PATH = "./resource/asset_info_set.csv"
ASSET_GROUP_PATH = "./resource/asset_group_info_set.csv"
ACCOUNT_PATH = "./resource/account_info_set.csv"
BROKERAGE_PATH = "./resource/brokerage_info_set.csv"


def insert_user():
    """
    유저 데이터 생성(CSV)
    중복 유저는 제외하고 데이터 생성
    """

    with open(USER_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            user_name = row[0]
            password = row[1]

            user = User.objects.filter(user_name=user_name)
            if user:
                continue
            else:
                User.objects.create(user_name=user_name, password=password)

    print("SECCESSED UPLOAD USER DATA!")


def insert_brokerage():
    """
    증권사 데이터 생성(CSV)
    중복 증권사는 제외하고 데이터 생성
    """

    with open(BROKERAGE_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            brokerage_name = row[0]

            brokerage = Brokerage.objects.filter(brokerage_name=brokerage_name)
            if brokerage:
                continue
            else:
                Brokerage.objects.create(
                    brokerage_name=brokerage_name,
                )

    print("SECCESSED UPLOAD BROKERAGE DATA!")


def insert_account():
    """
    계좌 데이터 생성(CSV)
    중복 계좌는 제외하고 생성 및 기존 DB 변동사항 발생 시 데이터 업데이트
    """

    with open(ACCOUNT_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            account_name = row[0]
            account_number = row[1]
            investment_principal = row[2]
            user_id = row[3]
            brokerage_id = row[4]
            user = User.objects.get(id=user_id)
            brokerage = Brokerage.objects.get(id=brokerage_id)

            account = Account.objects.filter(
                account_name=account_name,
                account_number=account_number,
                investment_principal=investment_principal,
            )
            if account:
                continue
            else:
                Account.objects.update_or_create(
                    account_name=account_name,
                    account_number=account_number,
                    investment_principal=investment_principal,
                    user=user,
                    brokerage=brokerage,
                )

    print("SECCESSED UPLOAD ACCOUNT DATA!")


def insert_asset_group():
    """
    자산 그룹 데이터 생성(CSV)
    중복 자산 그룹은 제외하고 데이터 생성
    """

    with open(ASSET_GROUP_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            asset_name = row[0]

            asset_group = AssetGroup.objects.filter(asset_name=asset_name)
            if asset_group:
                continue
            else:
                AssetGroup.objects.create(asset_name=asset_name)

    print("SECCESSED UPLOAD GROUP DATA!")


def insert_stock():
    """
    주식 데이터 생성(CSV)
    중복 주식은 제외하고 생성 및 기존 DB 변동사항 발생 시 데이터 업데이트
    """

    with open(STOCK_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            stock_name = row[0]
            ISIN = row[1]
            current_price = row[2]
            group_id = row[3]
            group = AssetGroup.objects.get(id=group_id)

            stock = Stock.objects.filter(
                stock_name=stock_name, ISIN=ISIN, current_price=current_price
            )
            if stock:
                continue
            else:
                Stock.objects.update_or_create(
                    stock_name=stock_name,
                    ISIN=ISIN,
                    current_price=current_price,
                    group=group,
                )

    print("SECCESSED UPLOAD STOCK DATA!")


def insert_asset():
    """
    자산 데이터 생성(CSV)
    중복 자산은 제외하고 생성 및 기존 DB 변동사항 발생 시 데이터 업데이트
    """

    with open(ASSET_PATH) as csv_file:
        data_reader = csv.reader(csv_file)
        next(data_reader, None)
        for row in data_reader:
            quantity = row[0]
            account_id = row[1]
            stock_id = row[2]
            account = Account.objects.get(id=account_id)
            stock = Stock.objects.get(id=stock_id)

            asset = Asset.objects.filter(
                quantity=quantity, account=account, stock=stock
            )
            if asset:
                continue
            else:
                Asset.objects.update_or_create(
                    quantity=quantity,
                    account=account,
                    stock=stock,
                )

    print("SECCESSED UPLOAD ASSET DATA!")


insert_user()
insert_brokerage()
insert_account()
insert_asset_group()
insert_stock()
insert_asset()
