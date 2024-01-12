
from django.urls import path, re_path
from . import views

urlpatterns = [

    path('test/', views.test, name='test'),
    path('', views.dashboard, name='home'),

    #URL's Clientes------------------------------------------------------------------------>
    path('clientes/', views.clientes, name='clientes'),
    path('clientes/crear', views.clienteCrear, name='cliente_crear'),
    path('clientes/<str:pk>/editar', views.clienteEditar, name='cliente_editar'),
    path('clientes/<str:pk>/eliminar', views.clienteEliminar, name='cliente_eliminar'),

    #URL's Órdenes------------------------------------------------------------------------->
    path('ordenes/', views.ordenes, name='ordenes'),
    path('ordenes/crear', views.ordenCrear, name='orde_crear'),
    path('ordenes/<str:pk>/editar', views.ordenEditar, name='orden_editar'),
    path('ordenes/<str:pk>/eliminar', views.ordenEliminar, name='orden_eliminar'),
    path('generate-excel/', views.download_excel, name='generate-excel'),

    #URL's Productos----------------------------------------------------------------------->
    path('productos/', views.productos, name='productos'),
    path('productos/crear', views.productoCrear, name='producto_crear'),
    path('productos/<str:pk>/editar', views.productoEditar, name='producto_editar'),
    path('productos/<str:pk>/eliminar', views.productoEliminar, name='producto_eliminar'),

]
