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
