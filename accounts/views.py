import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

from .models import Account, Deposit, User
from stocks.models import Asset

from .serializers import (
    AssetSerializer,
    InvestmentDetailSerializer,
    InvestmentSerializer,
    DepositCreateSerializer,
    SignInSerializer,
)

from rest_framework.generics import GenericAPIView


@api_view(("GET",))
def get_investment(request):
    """
    투자 화면 API
    클라이언트에서 유저 정보를 포함하여 요청
    """

    data = json.loads(request.body)

    if request.user.is_authenticated:
        account = Account.objects.get(id=data["user_id"])
        serializer = InvestmentSerializer(account)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET",))
def get_investment_detail(request):
    """
    투자 상세 화면 API
    """

    data = json.loads(request.body)

    if request.user.is_authenticated:
        account = Account.objects.get(id=data["user_id"])
        serializer = InvestmentDetailSerializer(account)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET",))
def get_own_stock(request):
    """
    보유 종목 화면 API
    """

    data = json.loads(request.body)

    if request.user.is_authenticated:
        asset = Asset.objects.filter(account_id=data["account_id"])
        serializer = AssetSerializer(asset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(("POST",))
@permission_classes([AllowAny])
def verificate_account(request):
    """
    계좌 입금 Phase1
    """

    data = json.loads(request.body)

    user_id = data["user"]
    account_id = data["account"]

    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)

        if not request.user.user_name == user.user_name:
            return Response(
                {"message": "본인 인증에 실패하였습니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        accounts = Account.objects.filter(user_id=user_id)
        re_account = Account.objects.get(id=account_id)

        for account in accounts:
            if account.account_number == re_account.account_number:
                print(account.account_number == re_account.account_number)
                break

        serializer = DepositCreateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            transfer_identifier = Deposit.objects.last().id

            return Response({"transfer_identifier": transfer_identifier})

        return Response(
            {"message": "인증에 실패하였습니다."}, status=status.HTTP_401_UNAUTHORIZED
        )
    return Response({"message": "인가 실패"})


class SignInView(GenericAPIView):
    """
    JWT를 사용한 로그인 기능
    """

    permission_classes = [AllowAny]
    serializer_class = SignInSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data
            return Response(
                {
                    "message": "로그인 되었습니다.",
                    "access_token": token["access"],
                    "refresh_token": token["refresh"],
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
