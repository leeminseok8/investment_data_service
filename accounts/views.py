from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Account

from .serializers import (
    InvestmentDetailSerializer,
    InvestmentSerializer,
)


@api_view(("GET",))
def get_investment(request):
    account = Account.objects.get(id=1)
    serializer = InvestmentSerializer(account)

    return Response(serializer.data, status=status.HTTP_200_OK)

    # if request.user.is_authenticated:
    #     account = Account.objects.all()
    #     serializer = InvestmentSerializer(account, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # else:
    #     return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    # return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(("GET",))
def get_investment_detail(request):
    account = Account.objects.get(id=1)
    serializer = InvestmentDetailSerializer(account)

    return Response(serializer.data, status=status.HTTP_200_OK)
