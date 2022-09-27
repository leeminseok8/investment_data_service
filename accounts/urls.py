from django.urls import path

from .views import (
    get_investment,
    get_investment_detail,
    get_own_stock,
    verificate_account,
    SignInView,
)


urlpatterns = [
    path("", get_investment),
    path("detail", get_investment_detail),
    path("own", get_own_stock),
    path("deposit1", verificate_account),
    path("signin", SignInView.as_view()),
]
