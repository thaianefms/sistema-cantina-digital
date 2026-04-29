from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import FormaPagamento

# View para listar formas de pagamento
@login_required
def listar_pagamentos(request):
    formas = FormaPagamento.objects.all()
    context = {'formas': formas}
    return render(request, 'pagamentos/listar.html', context)

# View para criar forma de pagamento
@login_required
def criar_pagamento(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao')
        ativo = request.POST.get('ativo') == 'on'
        
        try:
            FormaPagamento.objects.create(
                tipo=tipo,
                descricao=descricao,
                ativo=ativo
            )
            messages.success(request, 'Forma de pagamento cadastrada com sucesso!')
            return redirect('listar_pagamentos')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'pagamentos/criar.html')

# View para editar forma de pagamento
@login_required
def editar_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    
    if request.method == 'POST':
        forma.tipo = request.POST.get('tipo')
        forma.descricao = request.POST.get('descricao')
        forma.ativo = request.POST.get('ativo') == 'on'
        forma.save()
        messages.success(request, 'Forma de pagamento atualizada com sucesso!')
        return redirect('listar_pagamentos')
    
    context = {'forma': forma}
    return render(request, 'pagamentos/editar.html', context)

# View para deletar forma de pagamento
@login_required
def deletar_pagamento(request, id):
    forma = get_object_or_404(FormaPagamento, id=id)
    forma.delete()
    messages.success(request, 'Forma de pagamento deletada com sucesso!')
    return redirect('listar_pagamentos')