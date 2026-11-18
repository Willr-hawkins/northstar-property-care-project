from django.urls import path

from .views import QuoteSuccessView, QuoteView

app_name = "enquiries"

urlpatterns = [
    path("", QuoteView.as_view(), name="quote"),
    path("thanks/", QuoteSuccessView.as_view(), name="quote_success"),
]