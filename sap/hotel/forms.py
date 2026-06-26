from django import forms
from .models import Reserva


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'habitacion', 'fecha_entrada', 'fecha_salida', 'estado']

        # Le damos clases de Bootstrap para el diseño
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'habitacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_entrada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_salida': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    # Validación personalizada
    def clean(self):
        datos = super().clean()
        entrada = datos.get("fecha_entrada")
        salida = datos.get("fecha_salida")

        # vqlidamos la fecha
        if entrada and salida and salida <= entrada:
            raise forms.ValidationError("La fecha de salida no puede ser antes de la entrada.")

        return datos