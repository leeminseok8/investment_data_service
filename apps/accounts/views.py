import json
import hashlib
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Account, Deposit, Asset
from apps.users.models import User

from .serializers import (
    AssetSerializer,
    InvestmentDetailSerializer,
    InvestmentSerializer,
    DepositVerificateCreateSerializer,
    DepositUpdateSerializer,
)


@api_view(("GET",))
def get_investment(request):
    """
    투자 화면 API
    클라이언트에서 유저 정보를 포함하여 요청
    """

    if request.user.is_authenticated:
        account = get_object_or_404(Account, user_id=request.user.id)
        serializer = InvestmentSerializer(account)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET",))
def get_investment_detail(request):
    """
    투자 상세 화면 API
    """

    if request.user.is_authenticated:
        account = get_object_or_404(Account, user_id=request.user.id)
        serializer = InvestmentDetailSerializer(account)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET",))
def get_own_stock(request):
    """
    보유 종목 화면 API
    """

    if request.user.is_authenticated:
        account = get_object_or_404(Account, user_id=request.user.id)
        asset = Asset.objects.filter(account_id=account.id)
        serializer = AssetSerializer(asset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(("POST",))
def verificate_account(request):
    """
    계좌 입금 Phase1
    """

    data = json.loads(request.body)

    user_name = data["user_name"]
    account_number = data["account_number"]

    if request.user.is_authenticated:
        user = User.objects.get(user_name=user_name)

        if not request.user.user_name == user.user_name:
            return Response(
                {"message": "본인 인증에 실패하였습니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        accounts = Account.objects.filter(user_id=user.id)
        re_account = Account.objects.get(account_number=account_number)

        for account in accounts:
            if account.account_number == re_account.account_number:
                break

        deposit_create_data = {
            "amount": request.data["amount"],
            "user": user.id,
            "account": re_account.id,
        }

        serializer = DepositVerificateCreateSerializer(data=deposit_create_data)

        if serializer.is_valid():
            serializer.save()
            transfer_identifier = Deposit.objects.last().id

            return Response({"transfer_identifier": transfer_identifier})

        return Response(
            {"message": "인증에 실패하였습니다."}, status=status.HTTP_401_UNAUTHORIZED
        )
    return Response({"message": "로그인 또는 권한이 필요합니다."})


@api_view(("POST",))
def deposit_account(request):
    """
    계좌 입금 Phase2
    """

    data = json.loads(request.body)

    signature = data["signature"]
    transfer_identifier = data["transfer_identifier"]

    if request.user.is_authenticated:
        transfer_user = Deposit.objects.get(id=transfer_identifier)

        salt = "chicken"
        signature_str = f"{transfer_user.account.account_number}{transfer_user.user.user_name}{transfer_user.amount}{salt}"
        signature_hash = hashlib.sha3_512(signature_str.encode("utf-8")).hexdigest()

        if not signature_hash == signature:
            return Response({"message": "권한이 필요합니다."}, status=status.HTTP_403_FORBIDDEN)

        account = Account.objects.get(
            account_number=transfer_user.account.account_number
        )

        account_update_data = {
            "account_name": account.account_name,
            "account_number": account.account_number,
            "investment_principal": account.investment_principal + transfer_user.amount,
            "user": account.user.id,
            "brokerage": account.brokerage.id,
        }

        serializer = DepositUpdateSerializer(instance=account, data=account_update_data)

        if serializer.is_valid():
            serializer.save()

            return Response({"status": "True"}, status=status.HTTP_201_CREATED)
        return Response({"status": "False"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "로그인 또는 권한이 필요합니다."})
