from django.forms import *
from django.core.validators import *
from django.forms.models import inlineformset_factory
from django import forms

from .models import *

class OrdenForm(ModelForm):
    class Meta:
        model = Orden
        fields = (
            'cliente',
            'monto_cacelado',
            'monto_pagar',
            'completada'
            )
        widgets ={
            'cliente': Select(attrs={'class': 'form-control', 'placeholder':'', 'id':'cliente'}),
            'monto_cacelado': NumberInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'monto_cacelado'}),
            'monto_pagar': HiddenInput(attrs={'id':'monto_pagar'}),
            'completada': HiddenInput(attrs={'id':'completada'}),
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
            'precio'
            )
        widgets ={
            'nombre': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':''}),
            'tipo': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'tipo'}),
            'codigo': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'codigo'}),
            'stock': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'stock'}),
            'descuento': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'descuento'}),
            'precio': TextInput(attrs={'class': 'form-control', 'placeholder':'', 'id':'precio'}),
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

class ProductoSelect(forms.Select):
    def build_attrs(self, base_attrs, extra_attrs=None):
        attrs = super().build_attrs(base_attrs, extra_attrs)
        attrs.update({
            'class': 'form-control',
            'aria-label': 'Tipo de material',
        })
        return attrs

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(name, value, label, selected, index, subindex, attrs)

        if value:
            option['attrs']['data-price'] = value.instance.precio
            option['attrs']['data-stock'] = value.instance.stock
        return option

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
            'producto': ProductoSelect(),
            'cantidad': NumberInput(attrs={'class': 'form-control justify-content-center', 'min':'0', 'placeholder':'0'}),
        }, 
        extra=0,
        can_delete=True
    )

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for form in self.forms:
        form.fields['producto'].queryset = Producto.objects.all()
        form.fields['producto'].widget.attrs['class'] += ' producto-field'
