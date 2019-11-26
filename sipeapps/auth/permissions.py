from rest_framework.permissions import BasePermission

from sipeapps.auth.models import Usuario


class CheckPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            if not isinstance(request.user, Usuario):
                return False

            if request.user.is_admin:
                return True

            classe_permissao = str(type(view).__name__).lower()
            metodo_permissao = str(view.action).lower()
            permissao_necessaria = '{}.{}'.format(classe_permissao, metodo_permissao)

            try:
                permissoes_publicas = [str(p).lower() for p in view.public_permissions]
            except AttributeError:
                permissoes_publicas = []

            if metodo_permissao in permissoes_publicas:
                return True

            permissoes_do_usuario = request.user.perfil.permissoes.all().values_list('codigo', flat=True)
            return permissao_necessaria in permissoes_do_usuario
        return False
