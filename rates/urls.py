from django.urls import path

from . import views

urlpatterns = [
    path("rates/", views.RatesView.as_view(), name="all_rates"),
    path("tracked_rates/", views.TrackedRatesView.as_view(), name="tracked_rates"),
    path("currency/user_currency", views.TrackedQuoteView.as_view(), name="user_currency"),
    path("currency/<int:pk>/analytics/", views.RatesAnalyticView.as_view(), name="analytic"),
]
