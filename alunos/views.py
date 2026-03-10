from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Aluno

# View para listar alunos
def listar_alunos(request):
    alunos = Aluno.objects.all()
    context = {'alunos': alunos}
    return render(request, 'alunos/listar.html', context)

# View para criar aluno
def criar_aluno(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        matricula = request.POST.get('matricula')
        turma = request.POST.get('turma')
        
        try:
            Aluno.objects.create(nome=nome, matricula=matricula, turma=turma)
            messages.success(request, 'Aluno cadastrado com sucesso!')
            return redirect('listar_alunos')
        except Exception as e:
            messages.error(request, f'Erro ao cadastrar: {str(e)}')
    
    return render(request, 'alunos/criar.html')

# View para editar aluno
def editar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    
    if request.method == 'POST':
        aluno.nome = request.POST.get('nome')
        aluno.matricula = request.POST.get('matricula')
        aluno.turma = request.POST.get('turma')
        aluno.save()
        messages.success(request, 'Aluno atualizado com sucesso!')
        return redirect('listar_alunos')
    
    context = {'aluno': aluno}
    return render(request, 'alunos/editar.html', context)

# View para deletar aluno
def deletar_aluno(request, id):
    aluno = get_object_or_404(Aluno, id=id)
    aluno.delete()
    messages.success(request, 'Aluno deletado com sucesso!')
    return redirect('listar_alunos')