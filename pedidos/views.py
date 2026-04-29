from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido
from alunos.models import Aluno
from estoque.models import Alimento
from pagamentos.models import FormaPagamento

# View para listar pedidos
@login_required
def listar_pedidos(request):
    pedidos = Pedido.objects.all().select_related('aluno', 'alimento', 'forma_pagamento')
    context = {'pedidos': pedidos}
    return render(request, 'pedidos/listar.html', context)

# View para criar pedido
@login_required
def criar_pedido(request):
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        alimento_id = request.POST.get('alimento')
        quantidade = int(request.POST.get('quantidade', 1))  # Converter para int
        forma_pagamento_id = request.POST.get('forma_pagamento')
        status = request.POST.get('status')
        
        try:
            aluno = Aluno.objects.get(id=aluno_id)
            alimento = Alimento.objects.get(id=alimento_id)
            forma_pagamento = FormaPagamento.objects.get(id=forma_pagamento_id)
            
            # Validação de estoque
            if alimento.quantidade_disponivel < quantidade:
                messages.error(request, f'Estoque insuficiente! Apenas {alimento.quantidade_disponivel} unidades de {alimento.nome} disponíveis.')
                return redirect('criar_pedido')
            
            # Baixa no estoque
            alimento.quantidade_disponivel -= quantidade
            alimento.save()
            
            pedido = Pedido.objects.create(
                aluno=aluno,
                alimento=alimento,
                quantidade=quantidade,
                forma_pagamento=forma_pagamento,
                status=status
            )
            
            messages.success(request, 'Pedido criado com sucesso!')
            return redirect('listar_pedidos')
        except Exception as e:
            messages.error(request, f'Erro ao criar pedido: {str(e)}')
    
    alunos = Aluno.objects.all()
    alimentos = Alimento.objects.filter(ativo=True)
    formas_pagamento = FormaPagamento.objects.filter(ativo=True)
    
    context = {
        'alunos': alunos,
        'alimentos': alimentos,
        'formas_pagamento': formas_pagamento,
    }
    return render(request, 'pedidos/criar.html', context)

# View para editar pedido
@login_required
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    
    if request.method == 'POST':
        pedido.aluno_id = request.POST.get('aluno')
        pedido.alimento_id = request.POST.get('alimento')
        pedido.quantidade = int(request.POST.get('quantidade', 1))  # Converter para int
        pedido.forma_pagamento_id = request.POST.get('forma_pagamento')
        pedido.status = request.POST.get('status')
        pedido.save()
        messages.success(request, 'Pedido atualizado com sucesso!')
        return redirect('listar_pedidos')
    
    alunos = Aluno.objects.all()
    alimentos = Alimento.objects.all()
    formas_pagamento = FormaPagamento.objects.all()
    
    context = {
        'pedido': pedido,
        'alunos': alunos,
        'alimentos': alimentos,
        'formas_pagamento': formas_pagamento,
    }
    return render(request, 'pedidos/editar.html', context)
    
# View para deletar pedido
@login_required
def deletar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    messages.success(request, 'Pedido deletado com sucesso!')
    return redirect('listar_pedidos')


# View pública para o Cardápio (Client-side)
def cardapio(request):
    alimentos = Alimento.objects.filter(ativo=True, quantidade_disponivel__gt=0).order_by('nome')
    alunos = Aluno.objects.all().order_by('nome')
    formas_pagamento = FormaPagamento.objects.filter(ativo=True)
    
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        alimento_id = request.POST.get('alimento')
        quantidade = int(request.POST.get('quantidade', 1))
        forma_pagamento_id = request.POST.get('forma_pagamento')
        
        try:
            aluno = Aluno.objects.get(id=aluno_id)
            alimento = Alimento.objects.get(id=alimento_id)
            forma_pagamento = FormaPagamento.objects.get(id=forma_pagamento_id)
            
            # Validação de estoque
            if alimento.quantidade_disponivel < quantidade:
                messages.error(request, f'Poxa, temos apenas {alimento.quantidade_disponivel} unidades de {alimento.nome}.')
                return redirect('cardapio')
            
            # Baixa no estoque
            alimento.quantidade_disponivel -= quantidade
            alimento.save()
            
            Pedido.objects.create(
                aluno=aluno,
                alimento=alimento,
                quantidade=quantidade,
                forma_pagamento=forma_pagamento,
                status='pendente'
            )
            
            messages.success(request, '🎉 Seu pedido foi realizado com sucesso! Aguarde ser chamado.')
            return redirect('cardapio')
            
        except Exception as e:
            messages.error(request, f'Ops, ocorreu um erro: {str(e)}')
            
    context = {
        'alimentos': alimentos,
        'alunos': alunos,
        'formas_pagamento': formas_pagamento,
    }
    return render(request, 'pedidos/cardapio.html', context)
