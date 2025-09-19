from django.shortcuts import render
from django.http import JsonResponse
from warehousing.models import Commodity

def get_commodity_unit(request, pk):
    try:
        commodity = Commodity.objects.get(pk=pk)
        return JsonResponse({'unit_id': commodity.unit.id})
    except Commodity.DoesNotExist:
        return JsonResponse({'unit_id': None})

def get_filtered_commodities(request):
    ternal = request.GET.get("ternal")
    category_id = request.GET.get("category_id")

    qs = Commodity.objects.all()

    if ternal:
        qs = qs.filter(ternal=ternal)
    if category_id:
        qs = qs.filter(category_id=category_id)

    commodities = qs.values("id", "name")
    return JsonResponse(list(commodities), safe=False)

def home(request):
    return render(request, 'page/home.html')
