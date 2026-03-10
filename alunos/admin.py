from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'matricula', 'turma', 'data_criacao']
    search_fields = ['nome', 'matricula']
    list_filter = ['turma']
    ordering = ['nome']