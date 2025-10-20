from django import forms
from .models import Vaga, Mensagem


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos', 'salario', 'carga_horaria', 'ativo']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título da vaga'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição da vaga'}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Requisitos necessários'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 2500.00'}),
            'carga_horaria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 40h semanais'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite sua mensagem...'}),
        }
