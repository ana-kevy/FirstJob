from django.contrib.auth.decorators import user_passes_test


def grupo_required(nome_grupo):
    def check(user):
        return user.is_authenticated and user.groups.filter(name=nome_grupo).exists()

    return user_passes_test(check)
