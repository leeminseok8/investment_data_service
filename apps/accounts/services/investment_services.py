import hashlib

from apps.accounts.serializers import (
    AssetSerializer,
    DepositUpdateSerializer,
    DepositVerificateCreateSerializer,
    InvestmentDetailSerializer,
    InvestmentSerializer,
)
from apps.accounts.repository.get_object import (
    get_deposited_account,
    get_requested_account,
    get_transfer_identifier,
    get_user_account,
    get_user_all_account,
    get_user_own_asset,
)


def get_user_investment(user: int) -> InvestmentSerializer:
    """
    Args:
        user : 계좌를 소유한 유저의 FK

    Return:
        유저 이름, 계좌 이름, 계좌 번호, 증권사, 총 자산
    """

    account = get_user_account(user)
    serializer = InvestmentSerializer(account)

    return serializer.data


def get_user_investment_detail(user: int) -> InvestmentDetailSerializer:
    """
    Args:
        user : 계좌를 소유한 유저의 FK

    Return:
        유저 이름, 계좌 이름, 계좌 번호, 증권사, 총 자산, 총 수익, 수익률, 투자 원금
    """

    account = get_user_account(user)
    serializer = InvestmentDetailSerializer(account)

    return serializer.data


def get_user_own_stock(user: int) -> AssetSerializer:
    """
    Args:
        user : 계좌를 소유한 유저의 FK

    Return:
        자산군, 종목명, ISIN, 평가 금액
    """

    account = get_user_account(user)
    asset = get_user_own_asset(account.id)
    serializer = AssetSerializer(asset, many=True)

    return serializer.data


def create_transfer_identifier(user: int, account_number: str, amount: int) -> int:
    """
    Args:
        user : 계좌를 소유한 유저의 FK
        account_number : 클라이언트에게 요청받은 계좌번호
        amount : 클라이언트에게 요청받은 입금 금액

    Return:
        int : 거래정보 식별자 key 값
    """

    accounts = get_user_all_account(user)
    request_account = get_requested_account(account_number)

    for account in accounts:
        if account.account_number == request_account.account_number:
            break

    deposit_create_data = {
        "amount": amount,
        "user": user.id,
        "account": request_account.id,
    }

    serializer = DepositVerificateCreateSerializer(data=deposit_create_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    transfer_identifier = get_transfer_identifier()

    return transfer_identifier


def create_signature_hash(transfer_user: int) -> str:
    """
    Args:
        transfer_user : key 값에 일치하는 입금(Deposit) 객체의 pk

    Return:
        str : 계좌번호, 유저 이름, 입금 금액을 조합하여 암호화한 str
    """

    salt = "chicken"
    signature_str = f"{transfer_user.account.account_number}{transfer_user.user.user_name}{transfer_user.amount}{salt}"
    signature_hash = hashlib.sha3_512(signature_str.encode("utf-8")).hexdigest()

    return signature_hash


def update_deposit_account(transfer_user) -> None:
    """
    Args:
        transfer_user : key 값에 일치하는 입금(Deposit) 객체의 pk
    """

    account = get_deposited_account(transfer_user)
    account_update_data = {
        "account_name": account.account_name,
        "account_number": account.account_number,
        "investment_principal": account.investment_principal + transfer_user.amount,
        "user": account.user.id,
        "brokerage": account.brokerage.id,
    }

    serializer = DepositUpdateSerializer(instance=account, data=account_update_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
