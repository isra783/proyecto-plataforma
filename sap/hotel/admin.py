from django.contrib import admin

from hotel.models import habitat

from hotel.models import Reserva, Cliente

# Register your models here.
admin.site.register(habitat)
admin.site.register(Cliente)
admin.site.register(Reserva)
