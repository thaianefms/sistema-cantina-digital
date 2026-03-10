from django.urls import path
from . import views

urlpatterns = [
    path('pagamentos/', views.listar_pagamentos, name='listar_pagamentos'),
    path('pagamentos/criar/', views.criar_pagamento, name='criar_pagamento'),
    path('pagamentos/<int:id>/editar/', views.editar_pagamento, name='editar_pagamento'),
    path('pagamentos/<int:id>/deletar/', views.deletar_pagamento, name='deletar_pagamento'),
]
