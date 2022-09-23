from django.urls import path

from .views import get_investment, get_investment_detail


urlpatterns = [path("", get_investment), path("detail", get_investment_detail)]
