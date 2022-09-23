from rest_framework import serializers

from .models import Account
from stocks.models import Asset, AssetGroup, Stock


class AssetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetGroup
        fields = ["asset_name"]


class StockSerializer(serializers.ModelSerializer):
    group = AssetGroupSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ["stock_name", "ISIN", "group"]


class AssetSerializer(serializers.ModelSerializer):
    """
    보유 종목 화면 시리얼라이저
    응답 : 자산군, 종목명, ISIN, 평가 금액
    """

    stock = StockSerializer(read_only=True)
    stock_valuation = serializers.SerializerMethodField()  # 보유 종목 평가 금액

    class Meta:
        model = Asset
        fields = ["stock", "stock_valuation"]

    def get_stock_valuation(self, obj):
        stock_val = obj.quantity * obj.stock.current_price
        return stock_val


class InvestmentSerializer(serializers.ModelSerializer):
    """
    투자 화면 시리얼라이저
    응답 : 유저 이름, 계좌 이름, 계좌 번호, 증권사, 총 자산
    """

    user_name = serializers.SlugRelatedField(
        read_only=True, slug_field="user_name", source="user"
    )
    brokerage_name = serializers.SlugRelatedField(
        read_only=True, slug_field="brokerage_name", source="brokerage"
    )
    total_asset = serializers.SerializerMethodField()  # 총 자산

    class Meta:
        model = Account
        fields = [
            "id",
            "user_name",
            "account_name",
            "account_number",
            "brokerage_name",
            "total_asset",
        ]

    def get_total_asset(self, obj):
        assets = obj.asset_set.all()
        total_asset = 0

        for asset in assets:
            total_asset += asset.stock.current_price * asset.quantity

        return total_asset


class InvestmentDetailSerializer(InvestmentSerializer):
    """
    투자 상세 화면 시리얼라이저
    응답 : 유저 이름, 계좌 이름, 계좌 번호, 증권사, 총 자산, 총 수익, 수익률, 투자 원금
    """

    total_proceed = serializers.SerializerMethodField()  # 총 수익
    yeild = serializers.SerializerMethodField()  # 수익률

    class Meta:
        model = Account
        fields = [
            "id",
            "account_name",
            "account_number",
            "investment_principal",
            "brokerage_name",
            "total_asset",
            "total_proceed",
            "yeild",
        ]

    def get_total_proceed(self, obj):
        total_proceed = self.get_total_asset(obj) - obj.investment_principal
        return total_proceed

    def get_yeild(self, obj):
        return self.get_total_proceed(obj) / (obj.investment_principal * 100)
