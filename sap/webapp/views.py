
from django.shortcuts import render

from hotel.models import habitat

"""
def inicio(request):
    # 1. Traemos todas las habitaciones de la base de datos
    todas_habitaciones = habitat.objects.all()

    # 2. Creamos un diccionario vacío para agrupar la información
    habitaciones = {}

    # 3. Recorremos cada habitación para contarlas
    for hab in todas_habitaciones:
        # Obtenemos el nombre completo del tipo (Simple, Doble, etc.)
        tipo = hab.get_tipo_display()

        # Si el tipo de habitación no está en el resumen, lo agregamos empezando en 0
        if tipo not in habitaciones:
            habitaciones[tipo] = 0

        # Si esta habitación específica está disponible, sumamos 1 al contador de su tipo
        if hab.disponible:
            habitaciones[tipo] += 1

    # 4. Enviamos el resumen agrupado a tu HTML
    return render(request, 'bienvenido.html', {'resumen': habitaciones})
"""

"""
def inicio(request):
    todas_habitaciones = habitat.objects.all()
    # Cambiamos la estructura a: { 's': {'nombre': 'Simple', 'cantidad': 0} }
    resumen = {}

    for hab in todas_habitaciones:
        codigo = hab.tipo  # El código: 's', 'd', 'f', 'pv'
        nombre = hab.get_tipo_display()  # El nombre legible: 'simple', 'familiar'

        if codigo not in resumen:
            resumen[codigo] = {'nombre': nombre, 'cantidad': 0}

        if hab.disponible:
            resumen[codigo]['cantidad'] += 1

    return render(request, 'bienvenido.html', {'resumen': resumen})
"""

def inicio(request):
    # Traemos todas las habitaciones de la base de datos
    todas_habitaciones = habitat.objects.all()

    # Creamos un diccionario vacío para agrupar la información
    resumen = {}

    # Recorremos cada habitación para contarlas
    for hab in todas_habitaciones:
        # Guardamos el código del tipo (ej: 's', 'd', 'f', 'pv')
        codigo = hab.tipo

        # Obtenemos el nombre legible del tipo (ej: 'Simple', 'Doble', 'Familiar', 'Suite')
        nombre = hab.get_tipo_display()

        # Si el código aún no está en el diccionario, lo inicializamos
        if codigo not in resumen:
            resumen[codigo] = {"nombre": nombre, "cantidad": 0}

        # Si esta habitación está disponible, sumamos 1 a su contador
        if hab.disponible:
            resumen[codigo]["cantidad"] += 1

    # Calculamos el total de habitaciones disponibles sumando todas las cantidades
    total_disponibles = sum([datos["cantidad"] for datos in resumen.values()])

    # Renderizamos la plantilla 'bienvenido.html' enviando:
    # - resumen: el diccionario con nombre y cantidad por tipo
    # - total_disponibles: el número total de habitaciones disponibles
    return render(request, 'bienvenido.html', {
        'resumen': resumen,
        'total_disponibles': total_disponibles
    })


