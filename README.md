# 🍽️ Sistema Cantina Digital

Um sistema web para gerenciamento de pedidos de lanches em cantinas escolares.

## 🎯 Funcionalidades

- ✅ **Gerenciamento de Alunos** - Cadastro e controle de estudantes
- ✅ **Gerenciamento de Estoque** - Controle de alimentos e bebidas
- ✅ **Criação de Pedidos** - Alunos podem fazer pedidos
- ✅ **Formas de Pagamento** - Vale-Lanche, Vale-Bebida e PIX
- ✅ **Rastreamento de Status** - Acompanhe o status dos pedidos
- ✅ **Painel Admin** - Gerenciamento completo via Django Admin

## 🛠️ Tecnologias

- **Python 3.x**
- **Django 4.2**
- **SQLite3**
- **HTML5 & CSS3**

## 📋 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🚀 Como Instalar

### 1. Clone o Repositório

```bash
git clone https://github.com/seu-usuario/sistema-cantina-digital.git
cd sistema-cantina-digital
```

### 2. Crie um Ambiente Virtual

```bash
python -m venv venv
```

### 3. Ative o Ambiente Virtual

**Windows:**
```bash
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 5. Execute as Migrações

```bash
python manage.py migrate
```

### 6. Crie um Superusuário (Usuário Admin)

```bash
python manage.py createsuperuser
```

Siga as instruções para criar seu usuário.

### 7. Inicie o Servidor

```bash
python manage.py runserver
```

O sistema estará disponível em `http://127.0.0.1:8000/`

## 📖 Como Usar

### Acessar o Painel Admin

1. Vá para `http://127.0.0.1:8000/admin`
2. Faça login com seu superusuário
3. Gerencie alunos, alimentos, formas de pagamento e pedidos

### Usar o Sistema Web

- **Alunos:** `http://127.0.0.1:8000/alunos/`
- **Estoque:** `http://127.0.0.1:8000/estoque/`
- **Pagamentos:** `http://127.0.0.1:8000/pagamentos/`
- **Pedidos:** `http://127.0.0.1:8000/pedidos/`

## 📂 Estrutura do Projeto

```
sistema-cantina-digital/
├── config/                 # Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── alunos/                 # App de Alunos
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── estoque/                # App de Estoque
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── pedidos/                # App de Pedidos
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── pagamentos/             # App de Pagamentos
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── templates/              # Arquivos HTML
│   ├── base.html
│   ├── alunos/
│   ├── estoque/
│   ├── pedidos/
│   └── pagamentos/
├── manage.py               # Utilitário Django
├── requirements.txt        # Dependências do projeto
└── db.sqlite3             # Banco de Dados (não enviar)
```

## 🔐 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto (não enviar para o GitHub):

```
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
```

## 📝 Licença

Este projeto está sob a licença MIT.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)

## 📞 Contato

Para dúvidas ou sugestões, entre em contato!

---

**Desenvolvido com ❤️ para a cantina da escola**