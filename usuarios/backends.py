from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from empresa.models import Empresa

class MultiUserModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        try:
            empresa = Empresa.objects.get(username=username)
            if empresa.check_password(password):
                return empresa
        except Empresa.DoesNotExist:
            pass

        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            try:
                return Empresa.objects.get(pk=user_id)
            except Empresa.DoesNotExist:
                return None
            