from django.forms import *
from django.core.validators import *
from django.forms.models import inlineformset_factory

from .models import *

class OrdenForm(ModelForm):
    class Meta:
        model = Orden
        fields = (
            'cliente',
            'monto_cacelado',
            'monto_pagar',
            )
        widgets ={
            'cliente': Select(attrs={'class': 'form-control', 'placeholder':'', 'id':'cliente'}),
            'monto_cacelado': NumberInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'monto_cacelado'}),
            'monto_pagar': HiddenInput(attrs={'id':'monto_pagar'}),
        }

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = (
            'nombre',
            'tipo',
            'codigo',
            'stock',
            'descuento',
            )
        widgets ={
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':''}),
            'tipo': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'tipo'}),
            'codigo': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'codigo'}),
            'stock': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'stock'}),
            'descuento': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'descuento'}),
        }

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = (
            'ci',
            'ci_tipo',
            'nombre',
            'apellido',
            'telefono',
            'direccion',
            'email',
            )
        widgets ={
            'ci_tipo': Select(attrs={'class': 'form-control col-2', 'placeholder':'', 'id':'ci_tipo'}),
            'ci': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'ci'}),
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'nombre'}),
            'apellido': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'apellido'}),
            'telefono': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'telefono'}),
            'direccion': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'direccion'}),
            'email': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'email'}),
        }

class BaseInlineFormset(BaseInlineFormSet):
    def get_deletion_widget(self):
        return CheckboxInput(attrs={'class': 'form-check-input'})
        
OrdenItemFormset = inlineformset_factory(Orden, OrdenItem,
        fields = (
            'producto',
            'cantidad',
        ),
        formset=BaseInlineFormset,
        widgets = { 
            'producto': Select(attrs={'class': 'form-control', 'aria-label':'Tipo de material'}),
            'cantidad': NumberInput(attrs={'class': 'form-control justify-content-center', 'min':'0', 'placeholder':'0'}),
        }, 
        extra=0,
        can_delete=True
    )