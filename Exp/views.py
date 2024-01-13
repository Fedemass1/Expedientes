from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, CreateView, DeleteView

from .forms import PaseForm, AreaForm
from .models import Expedientes, ExpedientesPrueba, Pases, Areas
from django import forms


def index(request):
    return render(request, 'index6.html')


def index_prueba(request):
    return render(request, 'index6_prueba.html')


def list_expedientes(request):
    expedientes = list(Expedientes.objects.values())
    data = {'expedientes': expedientes}  # 'expedientes' (key) debe ser igual al nombre de mi tabla
    return JsonResponse(data)


def list_expedientes_prueba(request):
    expedientes_prueba = list(ExpedientesPrueba.objects.values())
    data = {'expedientes_prueba': expedientes_prueba}  # 'expedientes' (key) debe ser igual al nombre de mi tabla
    return JsonResponse(data)


class ExpActualizacion(UpdateView):
    model = Expedientes
    template_name = "editar_exp.html"
    fields = ['fecha', 'nro_exp', 'iniciador', 'objeto', 'nro_resol_rectorado', 'nro_resol_CS', 'observaciones']

    def get_success_url(self):
        print(f"get_success_url called. PK: {self.object.pk}")
        # Utiliza reverse_lazy para construir la URL en base de la función index. La función index dirige a '/Exp'
        return reverse_lazy('index')


class ExpActualizacionPrueba(UpdateView):
    model = ExpedientesPrueba
    template_name = "editar_exp.html"
    fields = ['fecha', 'nro_exp', 'iniciador', 'objeto', 'nro_resol_rectorado', 'nro_resol_CS', 'observaciones']

    def get_success_url(self):
        print(f"get_success_url called. PK: {self.object.pk}")
        # Utiliza reverse_lazy para construir la URL en base de la función index. La función index dirige a '/Exp'
        return reverse_lazy('index_prueba')

    # def get_form(self, form_class=None): Esta es una manera de personalizar el formulario. Aca no lo uso pq lo imlemente desde el html
    #     form = super().get_form(form_class)
    #     form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'}, format='%d/%m/%Y')
    #     return form


class ExpAgregarPrueba(CreateView):
    model = ExpedientesPrueba
    template_name = "agregar_exp.html"
    fields = ['fecha', 'nro_exp', 'iniciador', 'objeto', 'nro_resol_rectorado', 'nro_resol_CS', 'observaciones']
    success_url = '/Exp/prueba'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el último número de expediente
        ultimo_expediente = ExpedientesPrueba.objects.order_by('-nro_exp').first()

        # Calcular el siguiente número de expediente
        if ultimo_expediente:
            siguiente_nro_exp = ultimo_expediente.nro_exp + 1
        else:
            # Si no hay expedientes, empezar desde 1
            siguiente_nro_exp = 1

        # Agregar el siguiente número de expediente al contexto
        context['siguiente_nro_exp'] = siguiente_nro_exp

        return context

    def form_valid(self, form):
        # Asignar el siguiente número de expediente al formulario antes de guardarlo
        form.instance.nro_exp = self.get_context_data()['siguiente_nro_exp']
        return super().form_valid(form)


class ExpEliminar(DeleteView):
    model = ExpedientesPrueba
    template_name = "eliminar_exp.html"
    success_url = '/Exp/prueba/'


class Pase(CreateView):
    model = Pases
    form_class = PaseForm
    template_name = 'pases.html'
    success_url = '/Exp/prueba/'

    def form_invalid(self, form):  # Me sirve para mostrar por consola si el formulario en invalido
        print(form.errors)
        return super().form_invalid(form)

    def get_initial(self):
        initial = super().get_initial()
        initial['nro_exp'] = self.kwargs['pk']
        return initial


class CrearArea(CreateView):
    model = Areas
    template_name = 'crear_area.html'
    success_url = '/Exp/crear_area/'
    fields = ['area']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['areas'] = Areas.objects.all()
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Ocultar la etiqueta del campo "area"
        form.fields['area'].label = False
        return form




# class CrearArea(View):
#     template_name = 'crear_area.html'
#
#     def get(self, request):
#         form = AreaForm()
#         return render(request, self.template_name, {'form': form})
#
#     def post(self, request):
#         form = AreaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('lista_areas')  # Reemplaza 'lista_areas' con el nombre de tu URL para listar áreas
#         return render(request, self.template_name, {'form': form})