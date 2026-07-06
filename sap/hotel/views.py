from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from hotel.models import habitat
from hotel.forms import ReservaForm,Reserva



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


def reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            # Guardamos la reserva
            reserva = form.save(commit=False)
            reserva.estado = 'Pendiente'  # Aseguramos que inicie como pendiente
            reserva.save()

            messages.success(request, "Tu solicitud de reserva ha sido enviada con éxito.")
            return redirect('inicio')  # O redirige a donde prefieras
        else:
            # Si el formulario no es válido, el error de validación (la fecha)
            # se mostrará automáticamente en el template
            pass
    else:
        form = ReservaForm()

    return render(request, 'reserva.html', {'form': form})


def editar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    # --- CANDADO DE SEGURIDAD ---
    if reserva.estado == 'Aprobada' or reserva.estado == 'Completada':
        messages.error(request, "Bloqueado: No puedes editar una reserva que ya está en curso o finalizada.")
        return redirect('inicio')
        # ----------------------------

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "La reserva ha sido actualizada correctamente.")
            return redirect('inicio')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'editar.html', {'form': form, 'reserva': reserva})


def eliminar(request, id):
    reserva = get_object_or_404(Reserva, id=id)

    # --- CANDADO DE SEGURIDAD ---
    if reserva.estado == 'Aprobada' or reserva.estado == 'Completada':
        messages.error(request, "Bloqueado: No puedes eliminar una reserva que ya está aprobada.")
        return redirect('inicio')
    # ----------------------------

    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "La reserva ha sido eliminada del sistema.")
        return redirect('inicio')

    return render(request, 'eliminar.html', {'reserva': reserva})


def lista_reservas(request):
    # Extraemos todas las reservas de la base de datos
    reservas = Reserva.objects.all()
    # Las enviamos al nuevo HTML
    return render(request, 'lista_reservas.html', {'reservas': reservas})
