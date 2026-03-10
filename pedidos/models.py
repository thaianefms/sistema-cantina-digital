from django.db import models
from alunos.models import Aluno
from estoque.models import Alimento
from pagamentos.models import FormaPagamento

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('entregue', 'Entregue'),
    ]
    
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    alimento = models.ForeignKey(Alimento, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_pedido = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    def calcular_total(self):
        return self.alimento.preco * self.quantidade
    
    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Pedido {self.id} - {self.aluno.nome}"
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-data_pedido']