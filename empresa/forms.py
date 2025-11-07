# empresa/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Empresa

class EmpresaForm(UserCreationForm):
    class Meta:
        model = Empresa
        fields = ['username', 'email', 'password1', 'password2', 'nome', 'cnpj', 'endereco', 'telefone', 'descricao']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@empresa.com'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(xx) xxxxx-xxxx'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da empresa', 'rows': 3}),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj and not cnpj.replace('.', '').replace('/', '').replace('-', '').isdigit():
            raise forms.ValidationError('O CNPJ deve conter apenas números e símbolos válidos.')
        return cnpj