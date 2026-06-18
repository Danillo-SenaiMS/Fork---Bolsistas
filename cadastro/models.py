from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from base.models import DataModel
from base.managers import TenantManager
from accounts.models import User, Tenant


ESTADOS_CHOICES = [
    ('', '--- Selecione ---'),
    ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
    ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
    ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
]


def validar_maioridade(data_nascimento):
    if not data_nascimento:
        return
    idade = timezone.now().year - data_nascimento.year
    if idade < 18:
        raise ValidationError('É necessário ter pelo menos 18 anos.')


class CadastroBolsista(DataModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cadastro')

    telefone = models.CharField('Telefone', max_length=20, blank=True)
    data_nascimento = models.DateField('Data de nascimento', validators=[validar_maioridade])

    rua = models.CharField('Rua', max_length=255, blank=True)
    numero = models.CharField('Número', max_length=20, blank=True)
    bairro = models.CharField('Bairro', max_length=255, blank=True)
    cidade = models.CharField('Cidade', max_length=255, blank=True)
    estado = models.CharField('Estado', max_length=2, choices=ESTADOS_CHOICES, blank=True)

    curriculo = models.FileField('Currículo', upload_to='curriculos/', blank=True)
    foto = models.ImageField('Foto', upload_to='fotos/', blank=True)

    participacao_projetos_anos = models.PositiveIntegerField('Anos de experiência em projetos/pesquisa', default=0)
    participacao_congressos = models.BooleanField('Participação em congressos, feiras, eventos e palestras', default=False)
    resumo_anais = models.BooleanField('Resumo publicado em anais de eventos', default=False)
    artigo_completo_anais = models.BooleanField('Artigo completo publicado em anais de eventos', default=False)
    artigo_cientifico_nacional = models.BooleanField('Artigo científico ou capítulo de livro nacional publicado', default=False)
    artigo_cientifico_internacional = models.BooleanField('Artigo científico ou capítulo de livro internacional publicado', default=False)
    livro_patente = models.BooleanField('Livro publicado na área de interesse ou patente registrada', default=False)
    participacao_minicurso = models.BooleanField('Participação em minicurso (até 4 horas) na área de interesse', default=False)
    treinamento = models.BooleanField('Treinamento (acima de 4 horas) na área de interesse', default=False)
    pontuacao_previa = models.DecimalField('Pontuação prévia', max_digits=8, decimal_places=2, default=0)

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='cadastros')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Cadastro de Bolsista'
        verbose_name_plural = 'Cadastros de Bolsistas'

    def __str__(self):
        return f'Cadastro de {self.user.nome_completo}'

    @property
    def ultima_formacao(self):
        formacoes = list(self.formacoes.all())
        if not formacoes:
            return None
        return max(formacoes, key=lambda f: f.ano_conclusao or 0)


class FormacaoAcademica(DataModel):
    TIPO_CHOICES = [
        ('ensino_medio', 'Ensino Médio Completo'),
        ('graduacao', 'Graduação'),
        ('curso_tecnico', 'Curso Técnico'),
        ('especializacao', 'Especialização'),
        ('pos_graduacao', 'Pós-Graduação'),
        ('mba', 'MBA'),
        ('mestrado', 'Mestrado'),
        ('doutorado', 'Doutorado'),
        ('pos_doutorado', 'Pós-Doutorado'),
    ]

    STATUS_CHOICES = [
        ('', '---'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
    ]

    bolsista = models.ForeignKey(CadastroBolsista, on_delete=models.CASCADE, related_name='formacoes')
    tipo = models.CharField('Formação Acadêmica', max_length=20, choices=TIPO_CHOICES)
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, blank=True)
    instituicao = models.CharField('Nome da Instituição', max_length=255)
    curso = models.CharField('Curso', max_length=255, blank=True)
    area = models.CharField('Área', max_length=255, blank=True)
    ano_conclusao = models.IntegerField('Ano de conclusão', blank=True, null=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='formacoes')

    objects = TenantManager()

    class Meta:
        verbose_name = 'Formação Acadêmica'
        verbose_name_plural = 'Formações Acadêmicas'

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.instituicao}'

    @property
    def status_display(self):
        if self.tipo == 'ensino_medio':
            return ''
        return self.get_status_display()


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
