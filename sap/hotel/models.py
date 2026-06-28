from django.db import models
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
"campos de la tabla"
tipo_CHOICES = []
class habitat(models.Model):
    tipo_CHOICES = [
        ('s', 'simple'),
        ('d', 'doble'),
        ('f', 'familiar'),
        ('pv', 'suite'),
    ]
    numero = models.IntegerField()
    piso = models.IntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    capacidad = models.IntegerField()

    tipo = models.CharField(
        max_length=10,
        choices=tipo_CHOICES,
    )
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f'Habitación {self.numero} - Piso {self.piso} - Tipo: {self.get_tipo_display()} - ${self.precio}'

"aqui los datos personales "

class Cliente(models.Model):
    cedula_valida = RegexValidator(
        regex=r'^\d{1,10}$',
        message='La cédula debe contener solo 10 caracteres numericos.'
    )
    nom_vali = RegexValidator(
        regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
        message='Este campo solo debe contener letras y espacios.'
    )

    celu_val = RegexValidator(
        regex=r'^09\d{8}$',
        message='El número de celular debe tener 10 dígitos y empezar con 09.'
    )

    cedula = models.CharField(max_length=10,unique=True,validators=[cedula_valida])
    nombres = models.CharField(max_length=50, validators=[nom_vali])
    apellidos = models.CharField(max_length=50, validators=[nom_vali])
    telefono = models.CharField(max_length=10, validators=[celu_val])

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Reserva(models.Model):
    estado_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aprobada', 'Aprobada'),
        ('Completada', 'Completada (Check-out)'),
    ]

    # Relaciones (Claves Foráneas) requeridas por la rúbrica
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(habitat, on_delete=models.CASCADE)

    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    estado = models.CharField(max_length=20, choices=estado_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Reserva de {self.cliente} - Hab: {self.habitacion.numero} - Estado: {self.estado}"

    def save(self, *args, **kwargs):
        # 1. Primero guardamos la reserva de forma normal
        super().save(*args, **kwargs)

        # 2. Automatizamos el "interruptor" de la habitación
        if self.estado == 'Aprobada':
            self.habitacion.disponible = False
            self.habitacion.save()
        elif self.estado == 'Completada':
            self.habitacion.disponible = True
            self.habitacion.save()