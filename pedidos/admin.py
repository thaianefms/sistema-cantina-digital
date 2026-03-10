from django.contrib import admin
from .models import Pedido

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'aluno', 'alimento', 'quantidade', 'status', 'data_pedido', 'total']
    list_filter = ['status', 'data_pedido']
    search_fields = ['aluno__nome']
    ordering = ['-data_pedido']