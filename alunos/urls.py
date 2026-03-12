from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('alunos/', views.listar_alunos, name='listar_alunos'),
    path('alunos/criar/', views.criar_aluno, name='criar_aluno'),
    path('alunos/<int:id>/editar/', views.editar_aluno, name='editar_aluno'),
    path('alunos/<int:id>/deletar/', views.deletar_aluno, name='deletar_aluno'),
]