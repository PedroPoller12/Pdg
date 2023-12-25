from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *

@admin.register(Producto)
class ProductoAdmin(SimpleHistoryAdmin):
    ordering = ('id',)
    list_display = ('codigo', 'nombre', 'stock')
    history_list_diplay = ['status',]

@admin.register(Finanza)
class FinanzaAdmin(SimpleHistoryAdmin):
    ordering = ('cliente',)
    list_display = ('cliente', 'deuda', 'abono', 'estado')
    history_list_diplay = ['status',]

@admin.register(Cliente)
class ClienteAdmin(SimpleHistoryAdmin):
    ordering = ('id',)
    list_display = ('nombre', 'apellido', 'ci', 'finanza')
    history_list_diplay = ['status',]

@admin.register(Orden)
class OrdenAdmin(SimpleHistoryAdmin):
    ordering = ('id',)
    list_display = ('cliente', 'fecha_orden')
    history_list_diplay = ['status',]

@admin.register(OrdenItem)
class OrdenItemAdmin(SimpleHistoryAdmin):
    ordering = ('id',)
    list_display = ('producto', 'cantidad', 'fecha_salida')
    history_list_diplay = ['status',]



