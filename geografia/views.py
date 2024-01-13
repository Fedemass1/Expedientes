from django.http import JsonResponse
from django.shortcuts import render
from geografia.models import Pais, Ciudad


def index(request):
    return render(request, 'index5.html')


def get_paises(request):
    paises = list(Pais.objects.values())
    print(paises)

    if len(paises) > 0:
        data = {'message': 'Success', 'paises': paises}
    else:
        data = {'message': 'not found'}

    return JsonResponse(data)


def get_ciudades(request, pais_id):
    ciudades = list(Ciudad.objects.filter(pais_id=pais_id).values())
    if len(ciudades) > 0:
        data = {'message': 'Success', 'ciudades': ciudades}
    else:
        data = {'message': 'not found'}

    return JsonResponse(data)
