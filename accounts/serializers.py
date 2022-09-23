from rest_framework import serializers

from .models import Account


class InvestmentSerializer(serializers.ModelSerializer):
    user_name = serializers.SlugRelatedField(
        read_only=True, slug_field="user_name", source="user"
    )
    brokerage_name = serializers.SlugRelatedField(
        read_only=True, slug_field="brokerage_name", source="brokerage"
    )
    total_asset = serializers.SerializerMethodField()

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
    total_proceed = serializers.SerializerMethodField()
    yeild = serializers.SerializerMethodField()

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
