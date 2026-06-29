from django.db.models.signals import post_save
from django.dispatch import receiver

from cadastro.models import CadastroBolsista, SolicitacaoEdicao
from classificacao.models import AvaliacaoBolsista
from accounts.models import User
from base.mixins import GROUP_MANAGER
from .models import Notificacao


@receiver(post_save, sender=CadastroBolsista)
def notificar_cadastro(sender, instance, created, **kwargs):
    if created:
        Notificacao.objects.create(
            destinatario=instance.user,
            titulo='Cadastro realizado',
            mensagem='Seu cadastro de bolsista foi criado com sucesso.',
            tipo='cadastro',
        )


@receiver(post_save, sender=AvaliacaoBolsista)
def notificar_avaliacao(sender, instance, created, **kwargs):
    if created and instance.pontos > 0:
        Notificacao.objects.create(
            destinatario=instance.bolsista.user,
            titulo='Nova avaliação registrada',
            mensagem=(
                f'Você recebeu {instance.pontos} pontos no critério '
                f'"{instance.criterio.nome}".'
            ),
            tipo='sistema',
        )


@receiver(post_save, sender=SolicitacaoEdicao)
def notificar_solicitacao(sender, instance, created, **kwargs):
    if created and instance.status == 'pendente':
        gestores = User.objects.filter(
            groups__name=GROUP_MANAGER,
            is_active=True,
        )
        for gestor in gestores:
            Notificacao.objects.create(
                destinatario=gestor,
                titulo='Nova solicitação de edição',
                mensagem=f'{instance.bolsista.user.nome_completo} solicitou edição do campo "{instance.campo}".',
                tipo='solicitacao',
            )

    elif instance.status == 'aprovado':
        Notificacao.objects.create(
            destinatario=instance.bolsista.user,
            titulo='Solicitação aprovada',
            mensagem=f'Sua solicitação de edição do campo "{instance.campo}" foi aprovada.',
            tipo='solicitacao',
        )
    elif instance.status == 'rejeitado':
        Notificacao.objects.create(
            destinatario=instance.bolsista.user,
            titulo='Solicitação rejeitada',
            mensagem=f'Sua solicitação de edição do campo "{instance.campo}" foi rejeitada.',
            tipo='solicitacao',
        )
