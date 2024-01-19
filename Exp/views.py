from django import forms
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView, DetailView
from .forms import PaseForm, AreaForm, ExpedientesPruebaForm
from .models import Expedientes, ExpedientesPrueba, Pases, Areas, Iniciadores



def index(request):
    return render(request, 'index6.html')


def index_prueba(request):
    return render(request, 'index6_prueba.html')


def list_expedientes(request):
    expedientes = list(Expedientes.objects.values())
    data = {'expedientes': expedientes}  # 'expedientes' (key) debe ser igual al nombre de mi tabla
    return JsonResponse(data)


# Modifique mi función original de JsonResponse para que incluya el campo con el área en la que se encuentra el expediente
def list_expedientes_prueba(request):
    expedientes_prueba = ExpedientesPrueba.objects.all()
    expedientes_data = []

    for expediente_prueba in expedientes_prueba:
        pases = expediente_prueba.pases.order_by('-id')
        ultimo_pase = pases.first() if pases else None

        expediente_data = {
            'id': expediente_prueba.id,
            'fecha': expediente_prueba.fecha.strftime('%d/%m/%Y') if expediente_prueba.fecha else None,
            'nro_exp': expediente_prueba.nro_exp,
            'iniciador': expediente_prueba.iniciador.iniciador if expediente_prueba.iniciador else None,
            'sigla': expediente_prueba.iniciador.sigla if expediente_prueba.iniciador else None,
            'objeto': expediente_prueba.objeto,
            'nro_resol_rectorado': expediente_prueba.nro_resol_rectorado,
            'nro_resol_CS': expediente_prueba.nro_resol_CS,
            'observaciones': expediente_prueba.observaciones,
            'area_creacion': expediente_prueba.area_creacion.area if expediente_prueba.area_creacion else None,
            'ultimo_pase': {'area_receptora': ultimo_pase.area_receptora.area,
                            'fecha_pase': ultimo_pase.fecha_pase} if ultimo_pase else None,
        }

        expedientes_data.append(expediente_data)

    return JsonResponse({'expedientes_prueba': expedientes_data}, safe=False)


# La deje de usar ya que tuve que complejizarla con la función de arriba para poder traer el area receptora desde otra tabla
# def list_expedientes_prueba(request):
#     expedientes_prueba = list(ExpedientesPrueba.objects.values())
#     data = {'expedientes_prueba': expedientes_prueba}  # 'expedientes' (key) debe ser igual al nombre de mi tabla
#     return JsonResponse(data)


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

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            return response
        except IntegrityError:
            form.add_error(None, 'La combinación de número de expediente y año ya existe.')
            return self.form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date', 'class': 'form-control'},
                                                      format='%Y-%m-%d')
        return form

    def get_success_url(self):
        print(f"get_success_url called. PK: {self.object.pk}")
        # Utiliza reverse_lazy para construir la URL en base de la función index. La función index dirige a '/Exp'
        return reverse_lazy('index_prueba')

    # def get_form(self, form_class=None): Esta es una manera de personalizar el formulario. Aca no lo uso pq lo imlemente desde el html
    #     form = super().get_form(form_class)
    #     form.fields['fecha'].widget = forms.DateInput(attrs={'type': 'date'}, format='%d/%m/%Y')
    #     return form


class ExpAgregarPrueba(CreateView):
    template_name = "agregar_exp.html"
    form_class = ExpedientesPruebaForm
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
        # Obtener el área correspondiente al usuario actual
        area_usuario = self.request.user.area  # Ajusta esto según la relación entre Usuario y Área en tu modelo
        # Asignar el área al formulario antes de guardarlo
        form.instance.area_creacion = area_usuario
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

    #Este código no es necesario
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['nro_exp'] = self.kwargs['pk']
    #     print("Contexto", context['nro_exp'])
    #     return context

    def get_initial(self):
        expediente_prueba = ExpedientesPrueba.objects.get(pk=self.kwargs['pk'])

        initial = {
            'nro_exp_': expediente_prueba.nro_exp,
            'nro_exp': self.kwargs['pk'],
        }

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

class CrearIniciador(CreateView):
    model = Iniciadores
    template_name = 'crear_iniciador.html'
    success_url = '/Exp/crear_iniciador/'
    fields = ['iniciador', 'sigla']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['iniciadores'] = Iniciadores.objects.all()
        return context



class DetalleExpediente(DetailView):
    model = ExpedientesPrueba
    template_name = "lista_pases.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtén los pases ordenados por la fecha de pase de forma descendente (más nuevo primero)
        context['pases'] = self.object.pases.all().order_by('-fecha_pase')
        return context


