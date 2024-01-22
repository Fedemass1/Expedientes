from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from Exp.models import Pases, Areas, ExpedientesPrueba, Iniciadores


class PaseForm(forms.ModelForm):
    area_origen = forms.ModelChoiceField(queryset=Areas.objects.all(), required=False,
                                         widget=forms.Select(attrs={'class': 'form-control', 'readonly': True,
                                                                    'style': 'background-color: #e9ecef;'}),

                                         )

    area_receptora = forms.ModelChoiceField(queryset=Areas.objects.all(), required=False,
                                            widget=forms.Select(attrs={'class': 'form-select'}))
    fecha_pase = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M:%S'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'readonly': True, 'style': 'background-color: #e9ecef;'})

    )

    nro_exp = forms.ModelChoiceField(
        queryset=ExpedientesPrueba.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'readonly': True, 'style': 'background-color: #e9ecef;'}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(PaseForm, self).__init__(*args, **kwargs)
        nro_exp = self.initial.get('nro_exp')
        exp_year = self.initial.get('exp_year')
        print("nro_exp_", exp_year)

        ultimo_pase = Pases.objects.filter(nro_exp=nro_exp).order_by('-fecha_pase').first()
        # Set the current date and time for 'fecha_pase'
        self.initial['fecha_pase'] = timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S')

        if ultimo_pase is not None:
            self.fields['area_origen'].initial = ultimo_pase.area_receptora

        else:
            # Manejar el caso en que no existen pases para el expediente
            expediente_prueba = ExpedientesPrueba.objects.get(exp_year=exp_year)
            self.fields['area_origen'].initial = expediente_prueba.area_creacion
            print(f"Área de origen establecida como área de creación: {self.fields['area_origen'].initial}")

    def clean(self):
        cleaned_data = super().clean()
        area_origen = cleaned_data.get('area_origen')
        area_receptora = cleaned_data.get('area_receptora')

        if area_origen == area_receptora:
            self.add_error('area_receptora', "El área de origen y la receptora no pueden ser iguales.")
        if not area_receptora:
            self.add_error('area_receptora', "El área receptora no puede estar vacía")

        return cleaned_data

    class Meta:
        model = Pases
        fields = ['fecha_pase', 'nro_exp', 'area_origen', 'area_receptora']


class AreaForm(forms.ModelForm):
    class Meta:
        model = Areas
        fields = ['area']


class ExpedientesPruebaForm(forms.ModelForm):
    iniciador = forms.ModelChoiceField(queryset=Iniciadores.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = ExpedientesPrueba
        fields = ['fecha', 'nro_exp', 'iniciador', 'objeto', 'nro_resol_rectorado', 'nro_resol_CS', 'observaciones']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
