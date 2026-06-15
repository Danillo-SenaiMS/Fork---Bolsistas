from django.db import models
from base.models import DataModel
from base.managers import TenantManager
from accounts.models import User, Tenant


class Notificacao(DataModel):
    TIPO_CHOICES = [
        ('cadastro', 'Cadastro'),
        ('classificacao', 'Classificação'),
        ('solicitacao', 'Solicitação'),
        ('sistema', 'Sistema'),
    ]

    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    titulo = models.CharField('Título', max_length=255)
    mensagem = models.TextField('Mensagem')
    lido = models.BooleanField('Lido', default=False)
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='sistema')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='notificacoes')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-created_at']

    def __str__(self):
        return self.titulo
