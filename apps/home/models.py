# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from django.core.validators import *
from django.db.models import Sum, F


#Productos y sus cantidades 
class Producto(models.Model):

    nombre = models.CharField(max_length=30, null=True)
    tipo = models.CharField(max_length=20, null=True)
    codigo = models.CharField(max_length=8, validators=[MinLengthValidator(8)], unique=True, null=True)
    stock = models.IntegerField(validators=[int_list_validator(allow_negative=False)], null=True)
    descuento = models.IntegerField(validators=[int_list_validator(allow_negative=False)], default=0)
    precio = models.IntegerField(validators=[int_list_validator(allow_negative=False)], default=0)

    history = HistoricalRecords()

    class Meta:
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")

    def __str__(self):
        return f'{self.codigo} - {self.nombre}'

#Cliente y sus datos
class Cliente(models.Model):
    CI_OPT=(
        ('V', 'V'),
        ('E', 'E'),
        ('J', 'J')
    )
    STAT_OPT=(
        ('Abonado', 'Abonado'),
        ('Solvente', 'Solvente'),
    )

    ci = models.CharField(max_length=10, validators=[MinLengthValidator(7), RegexValidator(r'^[0-9]{1,2}[.]?[0-9]{3}[.]?[0-9]{3}$')], unique=True, null=True)
    ci_tipo =  models.CharField(default='V', max_length=1, choices=CI_OPT)
    nombre = models.CharField(max_length=30, null=False)
    apellido = models.CharField(max_length=30, null=False)                   #max_length=19 ^[\+]?[(]?[0-9]{1,2}[)]?[-\s]?[0-9]{3}[-\s]?[0-9]{3}[-\s]?[0-9]{2}[-\s]?[0-9]{2}$
    telefono = models.CharField(max_length=18, validators=[RegexValidator(r'^[\+]?[(]?[0-9]{1,2}[)]?[-\s]?[0-9]{3}[-\s]?[0-9]{3}[-\s]?[0-9]{4}$')], blank=False, null=False)
    direccion = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=30, blank=True, null=True)
    estatus = models.CharField(choices=STAT_OPT, max_length=8, default='Solvente')  
    
    history = HistoricalRecords()

    class Meta:
        verbose_name = ("Cliente")
        verbose_name_plural = ("Clientes")

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

#control de deuda y abono del cleinte

class Finanza(models.Model):

    cliente = models.OneToOneField('home.Cliente', on_delete=models.CASCADE, primary_key=True)
    abono = models.FloatField(default=0, validators=[MinValueValidator(0.0)], blank=True, null=True)
    deuda = models.FloatField(default=0, validators=[MinValueValidator(0.0)], blank=True, null=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = ("Finanza de Cliente")
        verbose_name_plural = ("Finanzas de Clientes")

    @property
    def estado(self):
        abono = self.abono or 0
        deuda = self.deuda or 0
        credit = abono - deuda
        sta = '+' if credit > 0 else ('' if credit < 0 else 0)
        if credit == 0:
            return 'Solvente'
        else:
            return f'{sta}{round(credit, 2)}' 

    def __str__(self):
        return f'{self.estado}'


#Oden de salida y asignación de prodcutos a un cliente, un cliente puede tener varias órdesnes que pueden tener varios productos
class Orden(models.Model):

    cliente = models.ForeignKey('home.Cliente', on_delete=models.SET_NULL, null=True)
    fecha_orden = models.DateTimeField(auto_now_add=True, null=True)
    monto_pagar = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    monto_cacelado = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True, default=0)
    completada = models.BooleanField(default=False, null=True)

    history = HistoricalRecords()
    
    class Meta:
        verbose_name = ("Orden")
        verbose_name_plural = ("Ordenes")
    

    def __str__(self):
        return f'{self.id} {self.cliente.nombre} {self.cliente.apellido} {self.fecha_orden}'

#Salida de Artículos de las órdenes, se usa para llevar la estaadiasticas de la salida de productos una orden puede tener varios porductos
class OrdenItem(models.Model):
    orden = models.ForeignKey('home.Orden', on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey('home.Producto', on_delete=models.RESTRICT, null=True)
    cantidad = models.IntegerField(validators=[int_list_validator(allow_negative=False), MinValueValidator(1)], null=False, default=0)#Cantidad de salida del producto, descuenta del stock del producto
    fecha_salida = models.DateTimeField(blank=True, null=True)#fecha de la salida del producto 

    history = HistoricalRecords()


    class Meta:
        verbose_name = ("Artículo Orden")
        verbose_name_plural = ("Artículos de Ordenes")

    def save(self, *args, **kwargs):
        # Primero, guardamos el objeto para evitar errores de referencia nula
        super().save(*args, **kwargs)

        # Luego, restamos la cantidad de la orden del stock del producto
        new_stock = self.producto.stock - self.cantidad
        self.producto.stock = new_stock
        self.producto.save()

    def __str__(self):
        return f'{self.orden.id} {self.fecha_orden} {self.producto.nombre}'


