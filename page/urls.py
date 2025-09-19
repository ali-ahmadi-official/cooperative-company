from django.urls import path
from .views import (
    get_commodity_unit,
    home,
)

urlpatterns = [
    path('', home, name='home'),
    path("get-commodity-unit/<int:pk>/", get_commodity_unit, name="get_commodity_unit"),
]
