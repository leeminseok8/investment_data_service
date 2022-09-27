from django.urls import path

from .views import (
    get_investment,
    get_investment_detail,
    get_own_stock,
    SignInView,
)


urlpatterns = [
    path("", get_investment),
    path("detail", get_investment_detail),
    path("own", get_own_stock),
    path("signin", SignInView.as_view()),
]
