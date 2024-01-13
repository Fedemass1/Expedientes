import json

from django.core import serializers
from django.core.serializers import serialize
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import UpdateView

from App.models import Programmer


def show_html(request):
    contexto = {

    }
    # return render(request,'index5.html', contexto)
    return render(request, 'index.html', contexto)


# Esta es la forma del video en youtube usando Javascript
# def list_programmers(request):
#     programmers = list(Programmer.objects.values())
#     data = {'programmers': programmers}
#     return JsonResponse(data)

def list_programmers(request):
    # Obtén tus datos del modelo o de donde sea necesario
    data = serializers.serialize('json', Programmer.objects.all())

    # Convierte la respuesta JSON de Django al formato esperado por DataTables
    data = {'data': json.loads(data)}

    return JsonResponse(data)

