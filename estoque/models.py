from django.db import models

class Alimento(models.Model):
    nome = models.CharField(max_length=100)
    quantidade_disponivel = models.IntegerField()
    preco = models.DecimalField(max_digits=5, decimal_places=2)
    ativo = models.BooleanField(default=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome} - {self.quantidade_disponivel} unidades"
    
    class Meta:
        verbose_name = "Alimento"
        verbose_name_plural = "Alimentos"
        ordering = ['nome']