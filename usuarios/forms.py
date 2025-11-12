from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import UsuarioAdaptado


class UsuarioAdaptadoForm(UserCreationForm):
    tipo_usuario = forms.ChoiceField(
        choices=[("candidato", "Candidato"), ("empresa", "Empresa")],
        label="Tipo de Usuário",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = UsuarioAdaptado
        fields = [
            "username",
            "email",
            "cpf",
            "endereco",
            "curriculo",
            "habilidades",
            "link_portfolio",
            "password1",
            "password2",
        ]
        widgets = {
            "username": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Nome de usuário"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "seu@email.com"}
            ),
            "cpf": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Digite seu CPF"}
            ),
            "endereco": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Endereço completo"}
            ),
            "curriculo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "habilidades": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Liste suas habilidades"}
            ),
            "link_portfolio": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "Link do seu portfólio"}
            ),
        }

    # >>>>> AQUI ADICIONEI
    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")

        if cpf:
            # verifica no banco se existe já um igual
            if UsuarioAdaptado.objects.filter(cpf=cpf).exists():
                raise forms.ValidationError("CPF já cadastrado no sistema.")

        return cpf

    # <<<<<<

    def save(self, commit=True):
        user = super().save(commit=False)
        tipo = self.cleaned_data["tipo_usuario"]

        # Define o tipo de usuário
        if tipo == "empresa":
            user.is_empresa = True
            user.is_candidato = False
        else:
            user.is_empresa = False
            user.is_candidato = True

        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome de usuário"}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"}),
    )
