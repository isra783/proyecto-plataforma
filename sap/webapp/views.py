
from django.shortcuts import render

from hotel.models import habitat


def inicio(request):
    lista_habitaciones = habitat.objects.all()
    return render(request, 'bienvenido.html',{'habitaciones': lista_habitaciones})


