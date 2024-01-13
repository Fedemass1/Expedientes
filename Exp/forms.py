from datetime import datetime

from django import forms
from django.utils import timezone
from Exp.models import Pases, Areas


class PaseForm(forms.ModelForm):
    area_origen = forms.ModelChoiceField(queryset=Areas.objects.all(), required=False,
                                         widget=forms.Select(attrs={'class': 'form-select'}))
    area_receptora = forms.ModelChoiceField(queryset=Areas.objects.all(), required=False,
                                            widget=forms.Select(attrs={'class': 'form-select'}))
    fecha_pase = forms.DateTimeField(
        initial=timezone.localtime(timezone.now()).strftime('%d/%m/%Y %H:%M:%S'),
        input_formats=['%d/%m/%Y %H:%M:%S'],
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'readonly': True, 'style': 'background-color: #e9ecef;'})
    )

    # nro_exp = forms.CharField(
    #     widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': True, 'style': 'background-color: #e9ecef;'})) Esta forma es
    # otra opción en lugar de incluirlo en la clase Meta. Se opta para usar la clase meta asi se usa una forma distinta y que se diferencia de la
    # usada para la fecha.

    class Meta:
        model = Pases
        fields = ['fecha_pase', 'nro_exp', 'area_origen', 'area_receptora']
        widgets = {
            'nro_exp': forms.TextInput(
                attrs={'class': 'form-control', 'readonly': True, 'style': 'background-color: #e9ecef;'}),
        }  # Podría también haberlo incluido dentro del Form.


class AreaForm(forms.ModelForm):
    class Meta:
        model = Areas
        fields = ['area']
