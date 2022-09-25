import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Account
from stocks.models import Asset

from .serializers import (
    AssetSerializer,
    InvestmentDetailSerializer,
    InvestmentSerializer,
)


@api_view(("GET",))
def get_investment(request):
    """
    투자 화면 API
    클라이언트에서 유저 정보를 포함하여 요청
    """

    data = json.loads(request.body)
    account = Account.objects.get(id=data["user_id"])
    serializer = InvestmentSerializer(account)

    return Response(serializer.data, status=status.HTTP_200_OK)

    """
    로그인을 통해 구현 시 is_authenticated를 통해 본인 인증을 거친 응답 로직
    """
    # if request.user.is_authenticated:
    #     account = Account.objects.all()
    #     serializer = InvestmentSerializer(account, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # else:
    #     return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    # return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET",))
def get_investment_detail(request):
    """
    투자 상세 화면 API
    """

    data = json.loads(request.body)
    account = Account.objects.get(id=data["user_id"])
    serializer = InvestmentDetailSerializer(account)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(("GET",))
def get_own_stock(request):
    """
    보유 종목 화면 API
    """

    data = json.loads(request.body)
    asset = Asset.objects.filter(account_id=data["account_id"])
    serializer = AssetSerializer(asset, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
