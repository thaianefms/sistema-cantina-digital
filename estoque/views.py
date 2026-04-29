from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Alimento

# View para listar alimentos
@login_required
def listar_alimentos(request):
    alimentos = Alimento.objects.all()
    context = {'alimentos': alimentos}
    return render(request, 'estoque/listar.html', context)

# View para criar alimento
@login_required
def criar_alimento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade_disponivel = request.POST.get('quantidade_disponivel')
        preco = request.POST.get('preco')
        ativo = request.POST.get('ativo') == 'on'
        
        try:
            Alimento.objects.create(
                nome=nome,
                quantidade_disponivel=quantidade_disponivel,
                preco=preco,
                ativo=ativo
            )
            messages.success(request, 'Alimento cadastrado com sucesso!')
            return redirect('listar_alimentos')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'estoque/criar.html')

# View para editar alimento
@login_required
def editar_alimento(request, id):
    alimento = get_object_or_404(Alimento, id=id)
    
    if request.method == 'POST':
        alimento.nome = request.POST.get('nome')
        alimento.quantidade_disponivel = request.POST.get('quantidade_disponivel')
        alimento.preco = request.POST.get('preco')
        alimento.ativo = request.POST.get('ativo') == 'on'
        alimento.save()
        messages.success(request, 'Alimento atualizado com sucesso!')
        return redirect('listar_alimentos')
    
    context = {'alimento': alimento}
    return render(request, 'estoque/editar.html', context)

# View para deletar alimento
@login_required
def deletar_alimento(request, id):
    alimento = get_object_or_404(Alimento, id=id)
    alimento.delete()
    messages.success(request, 'Alimento deletado com sucesso!')
    return redirect('listar_alimentos')