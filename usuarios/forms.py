from django import forms
from django.contrib.auth.models import User
from .models import Perfil

class SetupForm(forms.ModelForm):
    telefone = forms.CharField(max_length=20, required=True, label="Telefone de Contato")
    password = forms.CharField(widget=forms.PasswordInput, required=True, label="Senha")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('O e-mail é obrigatório.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está cadastrado.')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('O nome é obrigatório.')
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError('O sobrenome é obrigatório.')
        return last_name

    def save(self, commit=True):
        user = super().save(commit=False)
        # Usa o email como username
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        user.is_staff = True
        user.is_superuser = True
        if commit:
            user.save()
            Perfil.objects.create(user=user, telefone=self.cleaned_data['telefone'])
        return user
