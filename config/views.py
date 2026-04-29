from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Sum
from pedidos.models import Pedido
from estoque.models import Alimento

@login_required
def home(request):
    # Fuso horário atual do Django
    hoje = timezone.localtime(timezone.now()).date()
    
    # Pedidos de hoje
    pedidos_hoje = Pedido.objects.filter(data_pedido__date=hoje)
    total_pedidos = pedidos_hoje.count()
    
    # Faturamento de hoje
    faturamento_hoje = pedidos_hoje.aggregate(Sum('total'))['total__sum'] or 0
    
    # Estoque baixo (ex: menor ou igual a 10)
    estoque_baixo = Alimento.objects.filter(quantidade_disponivel__lte=10, ativo=True).order_by('quantidade_disponivel')
    
    context = {
        'total_pedidos': total_pedidos,
        'faturamento_hoje': faturamento_hoje,
        'estoque_baixo': estoque_baixo,
    }
    return render(request, 'home.html', context)
