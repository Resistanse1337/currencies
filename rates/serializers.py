from rest_framework import serializers

from rates.models import Currency, CurrencyHistory, TrackedQuote


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["id", "charcode"]


class RatesSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = CurrencyHistory
        fields = [
            "currency",
            "value",
            "date",
            "id",
        ]


class TrackedQuoteAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedQuote
        fields = [
            "currency",
            "threshold",
        ]
    
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class TrackedQuoteSerializer(serializers.Serializer):
    is_threshold_exceeded = serializers.BooleanField()
    threshold = serializers.DecimalField(max_digits=5, decimal_places=2)
    currency = serializers.CharField(source="currency.charcode")
    value = serializers.DecimalField(max_digits=5, decimal_places=2)


class RatesAnalyticSerializer(serializers.Serializer):
    threshold = serializers.DecimalField(max_digits=5, decimal_places=2)
    date_from = serializers.DateField()
    date_to = serializers.DateField()


class RatesAnalyticResultSerializer(serializers.Serializer):
    is_threshold_exceeded = serializers.BooleanField()
    date = serializers.DateField()
    value = serializers.DecimalField(max_digits=5, decimal_places=2)
    charcode = serializers.CharField(source="currency.charcode")
    id = serializers.IntegerField(source="currency.id")
    threshold_match_type = serializers.CharField()
    is_min_value = serializers.BooleanField()
    is_max_value = serializers.BooleanField()
    percentage_ratio = serializers.DecimalField(max_digits=5, decimal_places=2)
