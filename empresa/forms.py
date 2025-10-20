from django import forms
from .models import Empresa


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'endereco', 'telefone', 'email', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da empresa'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(xx) xxxxx-xxxx'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contato@empresa.com'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da empresa'}),
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if cnpj and not cnpj.replace('.', '').replace('/', '').replace('-', '').isdigit():
            raise forms.ValidationError('O CNPJ deve conter apenas números e símbolos válidos.')
        return cnpj
