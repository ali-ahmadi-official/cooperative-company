from django.urls import path
from .views import (
    get_commodity_unit, get_categories_by_ternal, get_commodity_categories_by_category, get_filtered_commodities,
    home,
)

urlpatterns = [
    path("get-commodity-unit/<int:pk>/", get_commodity_unit, name="get_commodity_unit"),
    path("get-categories-by-ternal/", get_categories_by_ternal, name="get_categories_by_ternal"),
    path("get-commodity-categories-by-category/", get_commodity_categories_by_category, name="get_commodity_categories_by_category"),
    path("get-filtered-commodities/", get_filtered_commodities, name="get_filtered_commodities"),
    path('', home, name='home'),
]
