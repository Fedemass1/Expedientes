# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUsers
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm


    # Otros ajustes de visualización en el listado y detalles del usuario
    list_display = ('username', 'email', 'area', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'area')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        # Agrega otros campos según tus necesidades
    )

    # Agregar el campo 'area' al formulario de creación en el admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('area',)}),
    )

# Registra el modelo y su administrador personalizado
admin.site.register(CustomUsers, CustomUserAdmin)
