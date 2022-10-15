from django.shortcuts import get_object_or_404
from apps.accounts.models import Account, Asset, Deposit
from apps.users.models import User


def get_user_account(user: int) -> Account:
    """
    Args:
        user : 계좌를 소유한 유저의 FK

    Return:
        Account : 유저가 소유한 계좌(Account) 객체
    """

    account = get_object_or_404(Account, user_id=user)
    return account


def get_user_own_asset(account_id: int) -> Asset:
    """
    Args:
        account_id : 유저가 소유한 계좌의 FK

    Return:
        Asset : 유저가 소유한 보유 주식(Asset) 목록 객체
    """

    asset = Asset.objects.filter(account_id=account_id)
    asset = asset.select_related("stock")
    return asset


def get_requested_user(user_name: str) -> User:
    """
    Args:
        user_name : 클라이언트에게 요청받은 유저 이름

    Return:
        User : 요청에 대한 응답 유저(User) 객체
    """

    user = User.objects.get(user_name=user_name)
    return user


def get_user_all_account(user: int) -> Account:
    """
    Args:
        user : 계좌를 소유한 유저의 FK

    Return:
        Account : 유저가 소유한 계좌(Account) 목록 객체
    """

    account = Account.objects.filter(user_id=user)
    return account


def get_requested_account(account_number: str) -> Account:
    """
    Args:
        account_number : 클라이언트에게 요청받은 계좌번호

    Return:
        Account : 요청에 대한 응답 계좌(Account) 객체
    """

    request_account = Account.objects.get(account_number=account_number)
    return request_account


def get_transfer_identifier() -> int:
    """
    Return:
        int : 거래정보 식별자 key 값
    """

    transfer_identifier = Deposit.objects.last().id
    return transfer_identifier


def get_deposit(transfer_identifier: int) -> Deposit:
    """
    Args:
        transfer_identifier : 거래정보 식별자 key 값

    Return:
        Deposit : key 값에 일치하는 입금(Deposit) 객체
    """

    transfer_user = Deposit.objects.get(id=transfer_identifier)
    return transfer_user


def get_deposited_account(transfer_user: Deposit) -> Account:
    """
    Args:
        transfer_user : key 갑에 일치하는 입금(Deposit) 객체

    Return:
        Account : 실제 입금하는 계좌(Account) 객체
    """

    account = Account.objects.get(account_number=transfer_user.account.account_number)
    return account
