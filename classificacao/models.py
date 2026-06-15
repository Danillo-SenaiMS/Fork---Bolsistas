from django.db import models
from base.models import DataModel
from base.managers import TenantManager
from accounts.models import User, Tenant
from editais.models import AplicacaoEdital


class CriterioClassificacao(DataModel):
    nome = models.CharField('Nome', max_length=255)
    descricao = models.TextField('Descrição', blank=True)
    peso = models.DecimalField('Peso', max_digits=10, decimal_places=2)
    ativo = models.BooleanField('Ativo', default=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='criterios')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Critério de Classificação'
        verbose_name_plural = 'Critérios de Classificação'

    def __str__(self):
        return self.nome


class Classificacao(DataModel):
    aplicacao = models.ForeignKey(AplicacaoEdital, on_delete=models.CASCADE, related_name='classificacoes')
    classificador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='classificacoes_feitas')
    pontuacao_total = models.DecimalField('Pontuação total', max_digits=10, decimal_places=2)
    observacoes = models.TextField('Observações', blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='classificacoes')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Classificação'
        verbose_name_plural = 'Classificações'

    def __str__(self):
        return f'{self.aplicacao.bolsista.user.nome_completo} - {self.pontuacao_total} pts'


class ClassificacaoCriterio(DataModel):
    classificacao = models.ForeignKey(Classificacao, on_delete=models.CASCADE, related_name='notas')
    criterio = models.ForeignKey(CriterioClassificacao, on_delete=models.CASCADE, related_name='notas')
    nota = models.DecimalField('Nota', max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Nota por Critério'
        verbose_name_plural = 'Notas por Critério'

    def __str__(self):
        return f'{self.criterio.nome}: {self.nota}'
