
from django.shortcuts import render

from hotel.models import habitat


def inicio(request):
    # 1. Capturamos el término de búsqueda por capacidad
    query = request.GET.get('q')

    # 2. Filtramos el modelo principal (habitat) si hay búsqueda
    if query:
        # Filtramos por capacidad exacta
        habitaciones = habitat.objects.filter(capacidad=query)
    else:
        # Si no hay búsqueda, traemos todas las habitaciones
        habitaciones = habitat.objects.all()

    # 3. Creamos el diccionario para agrupar la información
    resumen = {}

    # Recorremos la lista de habitaciones (que ya puede estar filtrada)
    for hab in habitaciones:
        codigo = hab.tipo
        nombre = hab.get_tipo_display()

        if codigo not in resumen:
            resumen[codigo] = {"nombre": nombre, "cantidad": 0}

        if hab.disponible:
            resumen[codigo]["cantidad"] += 1

    # 4. Calculamos el total de habitaciones disponibles
    total_disponibles = sum([datos["cantidad"] for datos in resumen.values()])

    # 5. Renderizamos 'inicio.html' con los datos procesados

    # Renderizamos la plantilla 'inicio.html' enviando los datos
    return render(request, 'bienvenido.html', {
        'resumen': resumen,
        'total_disponibles': total_disponibles
    })

