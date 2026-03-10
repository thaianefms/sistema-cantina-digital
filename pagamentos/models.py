from django.db import models

class FormaPagamento(models.Model):
    TIPO_CHOICES = [
        ('vale-lanche', 'Vale-Lanche'),
        ('vale-bebida', 'Vale-Bebida'),
        ('pix', 'PIX'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.get_tipo_display()
    
    class Meta:
        verbose_name = "Forma de Pagamento"
        verbose_name_plural = "Formas de Pagamento"
        ordering = ['tipo']
