from django import forms
from .models import Vaga


class VagaForm(forms.ModelForm):
    class Meta:
        model = Vaga
        fields = [
            "titulo",
            "descricao",
            "requisitos",
            "salario",
            "carga_horaria",
            "ativo",
            "area",
            "tipo_vaga",
            "tipo_contratacao",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "descricao": forms.Textarea(attrs={"class": "form-control"}),
            "requisitos": forms.Textarea(attrs={"class": "form-control"}),
            "salario": forms.NumberInput(attrs={"class": "form-control"}),
            "carga_horaria": forms.TextInput(attrs={"class": "form-control"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "area": forms.Select(attrs={"class": "form-control"}),
            "tipo_vaga": forms.Select(attrs={"class": "form-control"}),
            "tipo_contratacao": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "titulo": "Título da Vaga",
            "descricao": "Descrição",
            "requisitos": "Requisitos",
            "salario": "Salário",
            "carga_horaria": "Carga Horária", 
            "area": "Área de Atuação",
            "tipo_vaga": "Tipo de Vaga",
            "tipo_contratacao": "Tipo de Contratação",
        }

