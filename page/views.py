from django.shortcuts import render
from django.http import JsonResponse
from warehousing.models import RawMaterialCategory, CommodityCategory, Commodity

def get_commodity_unit(request, pk):
    try:
        commodity = Commodity.objects.get(pk=pk)
        return JsonResponse({'unit_id': commodity.unit.id})
    except Commodity.DoesNotExist:
        return JsonResponse({'unit_id': None})

def get_categories_by_ternal(request):
    ternal = request.GET.get("ternal")
    categories = RawMaterialCategory.objects.filter(ternal=ternal)
    data = list(categories.values("id", "name"))
    return JsonResponse(data, safe=False)

def get_commodity_categories_by_category(request):
    category_id = request.GET.get("category_id")
    commodity_categories = CommodityCategory.objects.filter(parent_id=category_id)
    data = list(commodity_categories.values("id", "name"))
    return JsonResponse(data, safe=False)

def get_filtered_commodities(request):
    commodity_category_id = request.GET.get("commodity_category_id")

    if not commodity_category_id:
        return JsonResponse([], safe=False)

    qs = Commodity.objects.filter(category_id=commodity_category_id)
    commodities = qs.values("id", "name")
    return JsonResponse(list(commodities), safe=False)

def home(request):
    return render(request, 'page/home.html')
