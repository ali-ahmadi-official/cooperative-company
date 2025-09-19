from django.urls import path
from .views import (
    get_commodity_unit, get_filtered_commodities,
    home,
)

urlpatterns = [
    path("get-commodity-unit/<int:pk>/", get_commodity_unit, name="get_commodity_unit"),
    path("get-filtered-commodities/", get_filtered_commodities, name="get_filtered_commodities"),
    path('', home, name='home'),
]
