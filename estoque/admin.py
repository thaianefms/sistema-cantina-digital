from django.contrib import admin
from .models import Alimento

@admin.register(Alimento)
class AlimentoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'quantidade_disponivel', 'preco', 'ativo']
    search_fields = ['nome']
    list_filter = ['ativo']
    ordering = ['nome']