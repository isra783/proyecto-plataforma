from django.http import HttpResponseBadRequest
from django.shortcuts import render
from hotel.models import habitat


# Create your views here.
"""
def hotel(request, tipo=None):
    if tipo:
        # Filtramos por el nombre del tipo (ej. 'Familiar')
        # Usamos el filtro de Django para comparar con el campo tipo
        hotel = habitat.objects.filter(tipo=tipo)
    else:
        # Si no viene un tipo, mostramos todo
        hotel = habitat.objects.all()

    return render(request, 'hotel.html', {'hotel': hotel, 'tipo_seleccionado': tipo})

"""
""""
def hotel(request, codigo=None):
    if codigo:
        # Filtramos directamente por el código que viene en la URL
        hotel = habitat.objects.filter(tipo=codigo)

        # Obtenemos el nombre completo para el título (opcional pero recomendado)
        # Esto busca en tu lista de choices el nombre legible (ej: 'simple')
        tipo_nom = dict(habitat.tipo_CHOICES).get(codigo, "Habitación")
    else:
        hotel = habitat.objects.all()
        tipo_nom = "Todas las Habitaciones"

    return render(request, 'hotel.html', {
        'hotel': hotel,
        'tipo_seleccionado': tipo_nom
    })

"""
"""
def hotel(request, codigo=None):
    codigos_validos = dict(habitat.tipo_CHOICES).keys()
    if codigo and codigo not in codigos_validos:
        return HttpResponseBadRequest("Tipo de habitación inválido")

    if codigo:
        hotel = habitat.objects.filter(tipo=codigo)
        tipo_nom = dict(habitat.tipo_CHOICES).get(codigo, "Habitación")
    else:
        hotel = habitat.objects.all()
        tipo_nom = "Todas las Habitaciones"

    return render(request, 'hotel.html', {
        'hotel': hotel,
        'tipo_seleccionado': tipo_nom
    })
"""

def hotel(request, codigo=None):
    # Definimos la vista 'hotel' que recibe:
    # - request: la petición HTTP
    # - codigo: opcional, viene desde la URL (ej: 's', 'd', 'f', 'pv')

    # Si viene un código (s, d, f, pv), filtramos
    if codigo:
        # Filtramos las habitaciones que coincidan con ese código
        hotel = habitat.objects.filter(tipo=codigo)

        # Obtenemos el nombre legible para el título (ej: 'Familiar')
        tipo_nom = dict(habitat.tipo_CHOICES).get(codigo, "Habitación")
    else:
        # Si no viene nada, traemos todas las habitaciones
        hotel = habitat.objects.all()

        # El título será "Todas las Habitaciones"
        tipo_nom = "Todas las Habitaciones"

    # Renderizamos la plantilla 'hotel.html' enviando:
    # - hotel: el conjunto de habitaciones filtradas (o todas)
    # - tipo_seleccionado: el nombre legible del tipo (o 'Todas las Habitaciones')
    return render(request, 'hotel.html', {
        'hotel': hotel,
        'tipo_seleccionado': tipo_nom
    })


