from drf_spectacular.utils import extend_schema
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from rates.models import CurrencyHistory, TrackedQuote
from rates.serializers import (RatesAnalyticResultSerializer,
                               RatesAnalyticSerializer, RatesSerializer,
                               TrackedQuoteAddSerializer,
                               TrackedQuoteSerializer)


class RatesView(ListAPIView):
    serializer_class = RatesSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["value"]

    def get_queryset(self):
        return CurrencyHistory.last_rates()


class TrackedRatesView(ListAPIView):
    serializer_class = TrackedQuoteSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["value"]

    def get_queryset(self):
        return TrackedQuote.tracked_quotes_for_user(self.request.user)


class TrackedQuoteView(CreateAPIView):
    serializer_class = TrackedQuoteAddSerializer
    permission_classes = [IsAuthenticated]


class RatesAnalyticView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatesAnalyticResultSerializer

    @extend_schema(parameters=[RatesAnalyticSerializer])
    def get(self, request: Request, pk: int):
        data = RatesAnalyticSerializer(data=request.query_params)
        data.is_valid(raise_exception=True)
        data = data.validated_data

        threshold = data["threshold"]
        date_from = data["date_from"]
        date_to = data["date_to"]

        currencies = CurrencyHistory.get_analytic(date_from, date_to, pk, threshold)

        result = RatesAnalyticResultSerializer(instance=currencies, many=True)
        result = result.data

        return Response(data=result, status=200)
