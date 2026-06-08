from .models import Notificacao


def criar_notificacao(destinatario, tipo_evento, mensagem, solicitacao=None):
    """Cria uma notificação no sistema para o destinatário informado."""
    Notificacao.objects.create(
        destinatario=destinatario,
        tipo_evento=tipo_evento,
        mensagem=mensagem,
        solicitacao=solicitacao,
    )
