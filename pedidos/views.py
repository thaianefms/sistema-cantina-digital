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
        quantidade = int(request.POST.get('quantidade', 1))  # Converter para int
        forma_pagamento_id = request.POST.get('forma_pagamento')
        status = request.POST.get('status')
        
        try:
            aluno = Aluno.objects.get(id=aluno_id)
            alimento = Alimento.objects.get(id=alimento_id)
            forma_pagamento = FormaPagamento.objects.get(id=forma_pagamento_id)
            
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
def deletar_pedido(request, id):
    pedido = get_object_or_404(Pedido, id=id)
    pedido.delete()
    messages.success(request, 'Pedido deletado com sucesso!')
    return redirect('listar_pedidos')