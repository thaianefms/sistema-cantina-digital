"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from config import views as config_views
from usuarios.views import setup_view, CustomLoginView, register_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('setup/', setup_view, name='setup'),
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),  # Rotas de logout e password reset nativas
    
    # Carregar o novo Dashboard
    path('', config_views.home, name='home'), 
    
    # Novas Rotas (Relatório e Webhook)
    path('relatorio/mensal/', config_views.relatorio_mensal_pdf, name='relatorio_mensal'),
    path('api/webhook/pedido/', config_views.webhook_pedido, name='webhook_pedido'),
    path('api/dashboard/realtime/', config_views.dashboard_realtime, name='dashboard_realtime'),
    
    path('', include('alunos.urls')),
    path('', include('estoque.urls')),
    path('', include('pedidos.urls')),
    path('', include('pagamentos.urls')),
]