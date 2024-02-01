# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import CustomUsers, Areas

class CustomUserCreationForm(UserCreationForm):
    area = forms.ModelChoiceField(queryset=Areas.objects.all(), label='Area')

    class Meta(UserCreationForm.Meta):
        model = CustomUsers
        fields = UserCreationForm.Meta.fields + ('area',)

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUsers
        fields = '__all__'  # Incluye todos los campos del modelo


