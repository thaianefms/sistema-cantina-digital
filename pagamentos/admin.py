from django.contrib import admin
from .models import FormaPagamento

@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'ativo']
    list_filter = ['ativo']
    ordering = ['tipo']