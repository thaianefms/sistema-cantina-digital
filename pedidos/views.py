from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Pedido
from alunos.models import Aluno
from estoque.models import Alimento
from pagamentos.models import FormaPagamento

# View para listar pedidos
def listar_pedidos(request):
    pedidos = Pedido.objects.all().select_related('aluno', 'alimento', 'forma_pagamento')
    context = {'pedidos': pedidos}
    return render(request, 'pedidos/listar.html', context)

# View para criar pedido
def criar_pedido(request):
    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        alimento_id = request.POST.get('alimento')
        quantidade = int(request.POST.get('quantidade', 1))
        forma_pagamento_id = request.POST.get('forma_pagamento')
        status = request.POST.get('status')
        
        try:
            aluno = Aluno.objects.get(id=aluno_id)
            alimento = Alimento.objects.get(id=alimento_id)
            forma_pagamento = FormaPagamento.objects.get(id=forma_pagamento_id)
            
            # Verificar se tem quantidade suficiente no estoque
            if alimento.quantidade_disponivel < quantidade:
                messages.error(request, f'Quantidade insuficiente! Disponível: {alimento.quantidade_disponivel}')
                return redirect('criar_pedido')
            
            # Criar o pedido
            pedido = Pedido.objects.create(
                aluno=aluno,
                alimento=alimento,
                quantidade=quantidade,
                forma_pagamento=forma_pagamento,
                status=status
            )
            
            # Diminuir a quantidade no estoque
            alimento.quantidade_disponivel -= quantidade
            alimento.save()
            
            messages.success(request, 'Pedido criado com sucesso! Estoque atualizado.')
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
def editar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    
    if request.method == 'POST':
        nova_quantidade = int(request.POST.get('quantidade', 1))
        novo_alimento_id = request.POST.get('alimento')
        
        try:
            # Se mudou o alimento ou a quantidade, precisamos ajustar o estoque
            if pedido.alimento.id != int(novo_alimento_id) or pedido.quantidade != nova_quantidade:
                
                # Devolver a quantidade anterior ao estoque
                alimento_antigo = pedido.alimento
                alimento_antigo.quantidade_disponivel += pedido.quantidade
                alimento_antigo.save()
                
                # Pegar o novo alimento
                novo_alimento = Alimento.objects.get(id=novo_alimento_id)
                
                # Verificar se tem quantidade suficiente no novo alimento
                if novo_alimento.quantidade_disponivel < nova_quantidade:
                    messages.error(request, f'Quantidade insuficiente! Disponível: {novo_alimento.quantidade_disponivel}')
                    return redirect('editar_pedido', id=pedido.id)
                
                # Diminuir a nova quantidade do novo alimento
                novo_alimento.quantidade_disponivel -= nova_quantidade
                novo_alimento.save()
            
            # Atualizar o pedido
            pedido.aluno_id = request.POST.get('aluno')
            pedido.alimento_id = novo_alimento_id
            pedido.quantidade = nova_quantidade
            pedido.forma_pagamento_id = request.POST.get('forma_pagamento')
            pedido.status = request.POST.get('status')
            pedido.save()
            
            messages.success(request, 'Pedido atualizado com sucesso! Estoque ajustado.')
            return redirect('listar_pedidos')
        except Exception as e:
            messages.error(request, f'Erro ao atualizar pedido: {str(e)}')
    
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
def deletar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    
    # Devolver a quantidade ao estoque
    alimento = pedido.alimento
    alimento.quantidade_disponivel += pedido.quantidade
    alimento.save()
    
    pedido.delete()
    messages.success(request, 'Pedido deletado com sucesso! Quantidade devolvida ao estoque.')
    return redirect('listar_pedidos')