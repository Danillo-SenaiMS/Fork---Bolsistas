from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from base.models import DataModel
from base.managers import TenantManager
from accounts.models import User, Tenant


def validar_maioridade(data_nascimento):
    if not data_nascimento:
        return
    idade = timezone.now().year - data_nascimento.year
    if idade < 18:
        raise ValidationError('É necessário ter pelo menos 18 anos.')


class CadastroBolsista(DataModel):
    GRAU_CHOICES = [
        ('fundamental', 'Ensino Fundamental'),
        ('medio', 'Ensino Médio'),
        ('superior', 'Ensino Superior'),
        ('pos', 'Pós-Graduação'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
        ('pos_doutorado', 'Pós-Doutorado'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cadastro')
    endereco = models.TextField('Endereço')
    data_nascimento = models.DateField('Data de nascimento', validators=[validar_maioridade])
    grau_academico = models.CharField('Grau acadêmico', max_length=20, choices=GRAU_CHOICES)
    curriculo = models.FileField('Currículo', upload_to='curriculos/', blank=True)
    foto = models.ImageField('Foto', upload_to='fotos/', blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='cadastros')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Cadastro de Bolsista'
        verbose_name_plural = 'Cadastros de Bolsistas'

    def __str__(self):
        return f'Cadastro de {self.user.nome_completo}'


class CursoSuperior(DataModel):
    GRAU_CHOICES = [
        ('tecnologo', 'Tecnólogo'),
        ('bacharelado', 'Bacharelado'),
        ('licenciatura', 'Licenciatura'),
    ]

    bolsista = models.ForeignKey(CadastroBolsista, on_delete=models.CASCADE, related_name='cursos_superiores')
    instituicao = models.CharField('Instituição', max_length=255)
    curso = models.CharField('Curso', max_length=255)
    grau = models.CharField('Grau', max_length=20, choices=GRAU_CHOICES)
    ano_conclusao = models.IntegerField('Ano de conclusão', blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='cursos_superiores')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Curso Superior'
        verbose_name_plural = 'Cursos Superiores'

    def __str__(self):
        return f'{self.curso} - {self.instituicao}'


class PosGraduacao(DataModel):
    TIPO_CHOICES = [
        ('pos_graduacao', 'Pós-Graduação'),
        ('mba', 'MBA'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
        ('pos_doutorado', 'Pós-Doutorado'),
    ]

    bolsista = models.ForeignKey(CadastroBolsista, on_delete=models.CASCADE, related_name='pos_graduacoes')
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)
    instituicao = models.CharField('Instituição', max_length=255)
    area = models.CharField('Área', max_length=255)
    ano_conclusao = models.IntegerField('Ano de conclusão', blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='pos_graduacoes')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Pós-Graduação'
        verbose_name_plural = 'Pós-Graduações'

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.area}'


class SolicitacaoEdicao(DataModel):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovado', 'Aprovado'),
        ('rejeitado', 'Rejeitado'),
    ]

    bolsista = models.ForeignKey(CadastroBolsista, on_delete=models.CASCADE, related_name='solicitacoes')
    campo = models.CharField('Campo', max_length=100)
    valor_original = models.TextField('Valor original')
    valor_novo = models.TextField('Valor novo')
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    revisado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='revisoes')
    data_revisao = models.DateTimeField('Data de revisão', blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='solicitacoes_edicao')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Solicitação de Edição'
        verbose_name_plural = 'Solicitações de Edição'

    def __str__(self):
        return f'{self.bolsista} - {self.campo} ({self.get_status_display()})'
