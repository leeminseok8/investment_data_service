import json
from urllib.request import Request

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.accounts.models import Account, Asset

from apps.accounts.services.investment_services import (
    create_signature_hash,
    create_transfer_identifier,
    get_user_investment,
    get_user_investment_detail,
    get_user_own_stock,
    update_deposit_account,
)

from .repository.get_object import (
    get_requested_user,
    get_deposit,
)


@api_view(("GET",))
def get_investment(request: Request) -> Account:
    """
    투자 화면 API
    """

    if request.user.is_anonymous:
        return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    account = get_user_investment(request.user)

    return Response(account, status=status.HTTP_200_OK)


@api_view(("GET",))
def get_investment_detail(request: Request) -> Account:
    """
    투자 상세 화면 API
    """

    if request.user.is_anonymous:
        return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    account = get_user_investment_detail(request.user)

    return Response(account, status=status.HTTP_200_OK)


@api_view(("GET",))
def get_own_stock(request: Request) -> Asset:
    """
    보유 종목 화면 API
    """

    if request.user.is_anonymous:
        return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    asset = get_user_own_stock(request.user)

    return Response(asset, status=status.HTTP_200_OK)


@api_view(("POST",))
def verificate_account(request: Request) -> int:
    """
    계좌 입금 Phase1
    Request:
        유저 이름, 계좌번호, 입금 금액

    Return:
        요청한 데이터 유효성 검사 후 일치하면 거래정보 식별자 key 응답
    """

    data = json.loads(request.body)

    user_name = data["user_name"]
    account_number = data["account_number"]
    amount = request.data["amount"]

    if request.user.is_anonymous:
        return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    user = get_requested_user(user_name)
    if not request.user.user_name == user.user_name:
        return Response(
            {"message": "본인 인증에 실패하였습니다."}, status=status.HTTP_401_UNAUTHORIZED
        )

    transfer_identifier = create_transfer_identifier(user, account_number, amount)

    return Response({"transfer_identifier": transfer_identifier})


@api_view(("POST",))
def deposit_account(request: Request) -> str:
    """
    계좌 입금 Phase2
    Request:
        signature : Phase1에서 검증된 데이터를 hashing한 str 값
        transfer_identifier : 거래정보 식별자 key 값

    Return:
        성공 : True
        실패 : False
    """

    data = json.loads(request.body)

    signature = data["signature"]
    transfer_identifier = data["transfer_identifier"]

    if request.user.is_anonymous:
        return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

    transfer_user = get_deposit(transfer_identifier)
    signature_hash = create_signature_hash(transfer_user)
    if not signature_hash == signature:
        return Response({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        update_deposit_account(transfer_user)
        return Response({"status": "True"}, status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({"status": "False"}, status=status.HTTP_400_BAD_REQUEST)
