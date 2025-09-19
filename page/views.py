from django.shortcuts import render
from django.http import JsonResponse
from warehousing.models import Commodity

def get_commodity_unit(request, pk):
    try:
        commodity = Commodity.objects.get(pk=pk)
        return JsonResponse({'unit_id': commodity.unit.id})
    except Commodity.DoesNotExist:
        return JsonResponse({'unit_id': None})

def home(request):
    return render(request, 'page/home.html')
