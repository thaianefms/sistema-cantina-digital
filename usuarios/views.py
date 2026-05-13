from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from .forms import SetupForm
from django.contrib.auth.views import LoginView

def setup_view(request):
    # Se já existir um usuário, redireciona para login
    if User.objects.exists():
        return redirect('login')

    if request.method == 'POST':
        form = SetupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SetupForm()
    
    return render(request, 'registration/setup.html', {'form': form})

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if User.objects.count() == 0:
            return redirect('setup')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # Chama o form_valid original para logar o usuário
        response = super().form_valid(form)
        
        # Verifica se o checkbox "lembrar_de_mim" foi marcado
        lembrar = self.request.POST.get('lembrar_de_mim', False)
        if lembrar:
            self.request.session.set_expiry(60 * 60 * 24 * 30)  # 30 dias
        else:
            self.request.session.set_expiry(0)  # Expira ao fechar navegador
            
        return response
