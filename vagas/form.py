from django import forms
from .models import Vaga, Mensagem


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = ['empresa', 'titulo', 'descricao', 'requisitos', 'salario', 'carga_horaria', 'ativo']
        widgets = {
            'empresa': forms.Select(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control'}),
            'salario': forms.NumberInput(attrs={'class': 'form-control'}),
            'carga_horaria': forms.TextInput(attrs={'class': 'form-control'}),
            'ativo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class MensagemForm(forms.ModelForm):
    class Meta:
        model = Mensagem
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite sua mensagem...'}),
        }
