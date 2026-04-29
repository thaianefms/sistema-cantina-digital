from django.urls import path
from . import views

urlpatterns = [
    path('cardapio/', views.cardapio, name='cardapio'),
    path('pedidos/', views.listar_pedidos, name='listar_pedidos'),
    path('pedidos/criar/', views.criar_pedido, name='criar_pedido'),
    path('pedidos/<int:id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/<int:id>/deletar/', views.deletar_pedido, name='deletar_pedido'),
]