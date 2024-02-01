from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            usuario = data.get("username")
            contrasenia = data.get("password")
            user = authenticate(username=usuario, password=contrasenia)

            if user is not None:
                login(request, user)
                return redirect("/Exp/prueba")
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')

    else:
        form = AuthenticationForm()

    contexto = {
        'form': form
    }

    return render(request, "login.html", contexto)



