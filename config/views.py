from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum
from pedidos.models import Pedido
from estoque.models import Alimento
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import json
from datetime import timedelta
import calendar

@login_required
def home(request):
    if User.objects.count() == 0:
        return redirect('setup')
        
    # Fuso horário atual do Django
    hoje = timezone.localtime(timezone.now()).date()
    
    # Pedidos de hoje
    pedidos_hoje = Pedido.objects.filter(data_pedido__date=hoje)
    total_pedidos = pedidos_hoje.count()
    
    # Faturamento de hoje
    faturamento_hoje = pedidos_hoje.aggregate(Sum('total'))['total__sum'] or 0
    
    # Estoque baixo (ex: menor ou igual a 10)
    estoque_baixo = Alimento.objects.filter(quantidade_disponivel__lte=10, ativo=True).order_by('quantidade_disponivel')
    
    # Faturamento dos Últimos 7 Dias para o Gráfico
    datas = []
    valores = []
    for i in range(6, -1, -1):
        dia = hoje - timedelta(days=i)
        faturamento_dia = Pedido.objects.filter(data_pedido__date=dia).aggregate(Sum('total'))['total__sum'] or 0
        datas.append(dia.strftime('%d/%m'))
        valores.append(float(faturamento_dia))
        
    # Top 5 Produtos Mais Vendidos (no mês atual)
    inicio_mes = hoje.replace(day=1)
    produtos_vendidos = Pedido.objects.filter(data_pedido__date__gte=inicio_mes)\
        .values('alimento__nome')\
        .annotate(quantidade_total=Sum('quantidade'))\
        .order_by('-quantidade_total')[:5]
        
    grafico_produtos_nomes = [p['alimento__nome'] for p in produtos_vendidos]
    grafico_produtos_qtds = [p['quantidade_total'] for p in produtos_vendidos]
        
    context = {
        'total_pedidos': total_pedidos,
        'faturamento_hoje': faturamento_hoje,
        'estoque_baixo': estoque_baixo,
        'grafico_datas': datas,
        'grafico_valores': valores,
        'grafico_produtos_nomes': grafico_produtos_nomes,
        'grafico_produtos_qtds': grafico_produtos_qtds,
    }
    return render(request, 'home.html', context)

@login_required
def relatorio_mensal_pdf(request):
    hoje = timezone.localtime(timezone.now()).date()
    inicio_mes = hoje.replace(day=1)
    # Pega o último dia do mês
    ultimo_dia = calendar.monthrange(hoje.year, hoje.month)[1]
    fim_mes = hoje.replace(day=ultimo_dia)
    
    pedidos_mes = Pedido.objects.filter(data_pedido__date__gte=inicio_mes, data_pedido__date__lte=fim_mes).order_by('data_pedido')
    total_mes = pedidos_mes.aggregate(Sum('total'))['total__sum'] or 0
    
    context = {
        'pedidos': pedidos_mes,
        'total_mes': total_mes,
        'mes_atual': hoje.strftime('%m/%Y')
    }
    return render(request, 'relatorio_pdf.html', context)

@csrf_exempt
@require_POST
def webhook_pedido(request):
    """
    Webhook para receber requisições de sistemas externos via POST.
    Exemplo de payload JSON:
    {
        "aluno_id": 1,
        "alimento_id": 2,
        "quantidade": 3,
        "forma_pagamento_id": 1,
        "token": "SECRET_WEBHOOK_123"
    }
    """
    try:
        dados = json.loads(request.body)
        
        # Validar um token simples de segurança (na vida real, idealmente validado via header Bearer)
        token_esperado = "SECRET_WEBHOOK_123" 
        if dados.get("token") != token_esperado:
            return JsonResponse({'erro': 'Não autorizado.'}, status=401)
            
        from alunos.models import Aluno
        from pagamentos.models import FormaPagamento
        
        aluno = Aluno.objects.get(id=dados['aluno_id'])
        alimento = Alimento.objects.get(id=dados['alimento_id'])
        forma_pagamento = FormaPagamento.objects.get(id=dados['forma_pagamento_id'])
        
        # Criar pedido
        pedido = Pedido.objects.create(
            aluno=aluno,
            alimento=alimento,
            quantidade=dados['quantidade'],
            forma_pagamento=forma_pagamento,
            status='pendente'
        )
        
        # Abater estoque
        alimento.quantidade_disponivel -= dados['quantidade']
        alimento.save()
        
        return JsonResponse({'sucesso': True, 'pedido_id': pedido.id, 'mensagem': 'Pedido criado via Webhook.'}, status=201)
        
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=400)

@login_required
def dashboard_realtime(request):
    hoje = timezone.localtime(timezone.now()).date()
    
    # KPIs
    pedidos_hoje = Pedido.objects.filter(data_pedido__date=hoje)
    total_pedidos = pedidos_hoje.count()
    faturamento_hoje = pedidos_hoje.aggregate(Sum('total'))['total__sum'] or 0
    estoque_baixo_count = Alimento.objects.filter(quantidade_disponivel__lte=10, ativo=True).count()
    
    # Gráfico 7 dias
    datas = []
    valores = []
    for i in range(6, -1, -1):
        dia = hoje - timedelta(days=i)
        faturamento_dia = Pedido.objects.filter(data_pedido__date=dia).aggregate(Sum('total'))['total__sum'] or 0
        datas.append(dia.strftime('%d/%m'))
        valores.append(float(faturamento_dia))
        
    return JsonResponse({
        'total_pedidos': total_pedidos,
        'faturamento_hoje': float(faturamento_hoje),
        'estoque_baixo_count': estoque_baixo_count,
        'datas': datas,
        'valores': valores
    })

