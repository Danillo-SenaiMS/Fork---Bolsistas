from django.db import models
from base.models import DataModel
from base.managers import TenantManager
from accounts.models import User, Tenant
from cadastro.models import CadastroBolsista


class Edital(DataModel):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('fechado', 'Fechado'),
        ('encerrado', 'Encerrado'),
    ]

    nome = models.CharField('Nome', max_length=255)
    descricao = models.TextField('Descrição')
    requisitos = models.TextField('Requisitos')
    data_abertura = models.DateTimeField('Data de abertura')
    data_fechamento = models.DateTimeField('Data de fechamento')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='aberto')
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='editais_criados')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='editais')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Edital'
        verbose_name_plural = 'Editais'
        ordering = ['-data_abertura']

    def __str__(self):
        return self.nome


class AplicacaoEdital(DataModel):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_analise', 'Em Análise'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    bolsista = models.ForeignKey(CadastroBolsista, on_delete=models.CASCADE, related_name='aplicacoes')
    edital = models.ForeignKey(Edital, on_delete=models.CASCADE, related_name='aplicacoes')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    data_aplicacao = models.DateTimeField('Data de aplicação', auto_now_add=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='aplicacoes')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Aplicação em Edital'
        verbose_name_plural = 'Aplicações em Editais'
        unique_together = ('bolsista', 'edital')

    def __str__(self):
        return f'{self.bolsista.user.nome_completo} - {self.edital.nome}'
