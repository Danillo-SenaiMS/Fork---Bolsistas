from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from faker import Faker

from accounts.models import User, Perfil, Tenant
from cadastro.models import CadastroBolsista, CursoSuperior, PosGraduacao
from editais.models import Edital, AplicacaoEdital
from classificacao.models import CriterioClassificacao, Classificacao, ClassificacaoCriterio

fake = Faker('pt_BR')


class Command(BaseCommand):
    help = 'Gera dados realistas para demonstracao'

    def handle(self, *args, **options):
        self.stdout.write('Limpando dados existentes...')
        ClassificacaoCriterio.objects.all().delete()
        Classificacao.objects.all().delete()
        CriterioClassificacao.objects.all().delete()
        AplicacaoEdital.objects.all().delete()
        Edital.objects.all().delete()
        CursoSuperior.objects.all().delete()
        PosGraduacao.objects.all().delete()
        CadastroBolsista.objects.all().delete()
        Perfil.objects.all().delete()
        User.objects.exclude(is_superuser=True).delete()
        Tenant.objects.all().delete()

        self.stdout.write('Criando tenants...')
        sesi = Tenant.objects.create(nome='SESI', dominio='sesi', ativo=True)
        senai = Tenant.objects.create(nome='SENAI', dominio='senai', ativo=True)

        for tenant in [sesi, senai]:
            self._seed_tenant(tenant)

        self.stdout.write(self.style.SUCCESS('Seed concluido com sucesso!'))

    def _seed_tenant(self, tenant):
        self.stdout.write(f'  Populando tenant: {tenant.nome}...')

        admin = self._criar_usuario('ADMIN', tenant)
        gestores = [self._criar_usuario('MANAGER', tenant) for _ in range(2)]
        bolsistas = [self._criar_usuario('COMMON', tenant) for _ in range(10)]

        cadastros = []
        for user in bolsistas[:6]:
            cad = self._criar_cadastro(user, tenant)
            cadastros.append(cad)

        criterios = self._criar_criterios(tenant)
        editais = self._criar_editais(tenant, admin)

        aplicacoes = []
        for i, cad in enumerate(cadastros):
            edital = editais[i % len(editais)]
            if not AplicacaoEdital.objects.filter(bolsista=cad, edital=edital).exists():
                apl = AplicacaoEdital.objects.create(
                    bolsista=cad,
                    edital=edital,
                    status='pendente' if i < 3 else 'em_analise',
                    tenant=tenant,
                )
                aplicacoes.append(apl)

        for i, apl in enumerate(aplicacoes[:4]):
            self._criar_classificacao(apl, gestores[i % len(gestores)], criterios, tenant)

    def _criar_usuario(self, tipo, tenant):
        primeiro_nome = fake.first_name()
        sobrenome = fake.last_name()
        email = f'{primeiro_nome.lower()}.{sobrenome.lower()}@{tenant.dominio}.com.br'
        user = User.objects.create_user(
            email=email,
            nome_completo=f'{primeiro_nome} {sobrenome}',
            password='123456',
        )
        user.is_active = True
        user.save()
        Perfil.objects.create(
            user=user,
            tipo=tipo,
            telefone=fake.phone_number() if tipo != 'ADMIN' else '',
            unidade=fake.bairro() if tipo != 'ADMIN' else '',
            tenant=tenant,
        )
        return user

    def _criar_cadastro(self, user, tenant):
        cad = CadastroBolsista.objects.create(
            user=user,
            endereco=fake.address(),
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=70),
            grau_academico=fake.random_element([
                'fundamental', 'medio', 'superior', 'pos',
                'mestrado', 'doutorado', 'pos_doutorado',
            ]),
            tenant=tenant,
        )
        if fake.boolean(chance_of_getting_true=60):
            CursoSuperior.objects.create(
                bolsista=cad,
                instituicao=fake.company(),
                curso=fake.random_element([
                    'Engenharia de Producao', 'Administracao', 'Ciencia da Computacao',
                    'Direito', 'Contabilidade', 'Psicologia',
                ]),
                grau=fake.random_element(['tecnologo', 'bacharelado', 'licenciatura']),
                ano_conclusao=fake.random_int(min=2000, max=2025),
                tenant=tenant,
            )
        if fake.boolean(chance_of_getting_true=40):
            PosGraduacao.objects.create(
                bolsista=cad,
                tipo=fake.random_element(['pos_graduacao', 'mba', 'mestrado']),
                instituicao=fake.company(),
                area=fake.random_element([
                    'Gestao de Projetos', 'Data Science', 'Educacao',
                    'Engenharia de Software', 'Marketing Digital',
                ]),
                ano_conclusao=fake.random_int(min=2010, max=2025),
                tenant=tenant,
            )
        return cad

    def _criar_criterios(self, tenant):
        dados = [
            ('Formacao Academica', 'Pontuacao por grau de formacao', 3.0),
            ('Experiencia Profissional', 'Tempo de experiencia na area', 2.5),
            ('Publicacoes', 'Artigos e publicacoes cientificas', 1.5),
            ('Cursos Complementares', 'Cursos de atualizacao na area', 1.0),
            ('Entrevista', 'Desempenho na entrevista tecnica', 2.0),
        ]
        criterios = []
        for nome, desc, peso in dados:
            c = CriterioClassificacao.objects.create(
                nome=nome,
                descricao=desc,
                peso=peso,
                ativo=True,
                tenant=tenant,
            )
            criterios.append(c)
        return criterios

    def _criar_editais(self, tenant, admin):
        dados = [
            ('Bolsa de Iniciacao Cientifica', 'Programa de iniciacao cientifica para estudantes de graduacao.', 'Estar matriculado em curso superior.'),
            ('Bolsa de Mestrado', 'Auxilio para alunos de mestrado em engenharia.', 'Ter sido aprovado em programa de mestrado.'),
            ('Bolsa de Doutorado', 'Auxilio para alunos de doutorado.', 'Ter sido aprovado em programa de doutorado.'),
        ]
        now = timezone.now()
        editais = []
        for nome, desc, req in dados:
            dias_atras = fake.random_int(min=5, max=30)
            dias_frente = fake.random_int(min=15, max=60)
            edital = Edital.objects.create(
                nome=nome,
                descricao=desc,
                requisitos=req,
                data_abertura=now - timezone.timedelta(days=dias_atras),
                data_fechamento=now + timezone.timedelta(days=dias_frente),
                status='aberto',
                criado_por=admin,
                tenant=tenant,
            )
            editais.append(edital)
        return editais

    def _criar_classificacao(self, aplicacao, gestor, criterios, tenant):
        classificacao = Classificacao.objects.create(
            aplicacao=aplicacao,
            classificador=gestor,
            pontuacao_total=0,
            observacoes=fake.sentence(nb_words=10),
            tenant=tenant,
        )
        pontuacao_total = 0.0
        for criterio in criterios:
            nota = fake.random_int(min=0, max=10)
            ClassificacaoCriterio.objects.create(
                classificacao=classificacao,
                criterio=criterio,
                nota=nota,
            )
            pontuacao_total += nota * float(criterio.peso)
        classificacao.pontuacao_total = pontuacao_total
        classificacao.save(update_fields=['pontuacao_total'])
