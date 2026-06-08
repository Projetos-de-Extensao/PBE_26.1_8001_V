# pyrefly: ignore [missing-import]
from rest_framework.permissions import BasePermission


class IsAluno(BasePermission):
    """Permite acesso apenas a usuários com perfil de Aluno."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'aluno')
        )


class IsCoordenador(BasePermission):
    """Permite acesso apenas a usuários com perfil de Coordenador."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'coordenador')
        )


class IsEmpresa(BasePermission):
    """Permite acesso apenas a usuários com perfil de Organização Parceira."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'organizacaoparceira')
        )


class IsCoordenadorOrReadOnly(BasePermission):
    """Coordenador pode tudo; outros perfis autenticados podem apenas ler."""

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return hasattr(request.user, 'coordenador')


class IsOwnerOrCoordenador(BasePermission):
    """Permite acesso ao dono do recurso (aluno) ou ao coordenador."""

    def has_object_permission(self, request, view, obj):
        if hasattr(request.user, 'coordenador'):
            return True
        if hasattr(obj, 'aluno') and hasattr(request.user, 'aluno'):
            return obj.aluno == request.user.aluno
        if hasattr(obj, 'solicitacao') and hasattr(request.user, 'aluno'):
            return obj.solicitacao.aluno == request.user.aluno
        if hasattr(obj, 'documento') and hasattr(request.user, 'aluno'):
            return obj.documento.solicitacao.aluno == request.user.aluno
        if hasattr(obj, 'usuario'):
            return obj.usuario == request.user
        return False
