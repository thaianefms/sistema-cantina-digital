from django.urls import path
from . import views

urlpatterns = [
    path('estoque/', views.listar_alimentos, name='listar_alimentos'),
    path('estoque/criar/', views.criar_alimento, name='criar_alimento'),
    path('estoque/<int:id>/editar/', views.editar_alimento, name='editar_alimento'),
    path('estoque/<int:id>/deletar/', views.deletar_alimento, name='deletar_alimento'),
]