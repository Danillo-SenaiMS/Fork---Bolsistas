from django.db.models.signals import post_save
from django.dispatch import receiver

from cadastro.models import CadastroBolsista, SolicitacaoEdicao
from classificacao.models import Classificacao
from .models import Notificacao


@receiver(post_save, sender=CadastroBolsista)
def notificar_cadastro(sender, instance, created, **kwargs):
    if created:
        Notificacao.objects.create(
            destinatario=instance.user,
            titulo='Cadastro realizado',
            mensagem='Seu cadastro de bolsista foi criado com sucesso.',
            tipo='cadastro',
            tenant=instance.tenant,
        )


@receiver(post_save, sender=Classificacao)
def notificar_classificacao(sender, instance, **kwargs):
    if instance.pontuacao_total > 0:
        bolsista = instance.aplicacao.bolsista.user
        edital = instance.aplicacao.edital.nome
        Notificacao.objects.create(
            destinatario=bolsista,
            titulo='Classificação publicada',
            mensagem=f'Sua classificação no edital "{edital}" foi publicada. '
                     f'Pontuação total: {instance.pontuacao_total} pts.',
            tipo='classificacao',
            tenant=instance.tenant,
        )


@receiver(post_save, sender=SolicitacaoEdicao)
def notificar_solicitacao(sender, instance, **kwargs):
    if instance.status == 'aprovado':
        Notificacao.objects.create(
            destinatario=instance.bolsista.user,
            titulo='Solicitação aprovada',
            mensagem=f'Sua solicitação de edição do campo "{instance.campo}" foi aprovada.',
            tipo='solicitacao',
            tenant=instance.tenant,
        )
    elif instance.status == 'rejeitado':
        Notificacao.objects.create(
            destinatario=instance.bolsista.user,
            titulo='Solicitação rejeitada',
            mensagem=f'Sua solicitação de edição do campo "{instance.campo}" foi rejeitada.',
            tipo='solicitacao',
            tenant=instance.tenant,
        )
