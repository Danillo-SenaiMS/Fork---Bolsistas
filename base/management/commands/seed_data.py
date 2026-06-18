from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction

from faker import Faker

from accounts.models import User, Perfil, Tenant
from cadastro.models import CadastroBolsista, FormacaoAcademica
from editais.models import EditalProvisorio, AplicacaoEdital
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
        EditalProvisorio.objects.all().delete()
        FormacaoAcademica.objects.all().delete()
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
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=70),
            tenant=tenant,
        )
        return user

    def _criar_cadastro(self, user, tenant):
        cad = CadastroBolsista.objects.create(
            user=user,
            rua=fake.street_name(),
            numero=str(fake.building_number()),
            bairro=fake.bairro(),
            cidade=fake.city(),
            estado=fake.random_element(['MS', 'SP', 'RJ', 'PR', 'RS']),
            telefone=fake.phone_number(),
            data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=70),
            tenant=tenant,
        )
        if fake.boolean(chance_of_getting_true=60):
            FormacaoAcademica.objects.create(
                bolsista=cad,
                tipo='graduacao',
                status=fake.random_element(['em_andamento', 'concluida']),
                instituicao=fake.company(),
                curso=fake.random_element([
                    'Engenharia de Producao', 'Administracao', 'Ciencia da Computacao',
                    'Direito', 'Contabilidade', 'Psicologia',
                ]),
                ano_conclusao=fake.random_int(min=2000, max=2025),
                tenant=tenant,
            )
        if fake.boolean(chance_of_getting_true=40):
            FormacaoAcademica.objects.create(
                bolsista=cad,
                tipo=fake.random_element(['especializacao', 'mba', 'mestrado']),
                status=fake.random_element(['em_andamento', 'concluida']),
                instituicao=fake.company(),
                area=fake.random_element([
                    'Gestao de Projetos', 'Data Science', 'Educacao',
                    'Engenharia de Software', 'Marketing Digital',
                ]),
                ano_conclusao=fake.random_int(min=2010, max=2025),
                tenant=tenant,
            )
        # Seed some boolean criteria randomly
        cad.participacao_projetos_anos = fake.random_int(min=0, max=15) if fake.boolean(chance_of_getting_true=50) else 0
        cad.participacao_congressos = fake.boolean(chance_of_getting_true=40)
        cad.resumo_anais = fake.boolean(chance_of_getting_true=30)
        cad.artigo_completo_anais = fake.boolean(chance_of_getting_true=25)
        cad.artigo_cientifico_nacional = fake.boolean(chance_of_getting_true=20)
        cad.artigo_cientifico_internacional = fake.boolean(chance_of_getting_true=10)
        cad.livro_patente = fake.boolean(chance_of_getting_true=5)
        cad.participacao_minicurso = fake.boolean(chance_of_getting_true=35)
        cad.treinamento = fake.boolean(chance_of_getting_true=30)
        cad.save()
        return cad

    def _criar_criterios(self, tenant):
        dados = [
            ('Graduação', 'graduacao', 'Pontuacao por possuir graduacao', None, 0),
            ('Mestrado', 'mestrado', 'Pontuacao por possuir mestrado', None, 0),
            ('Doutorado', 'doutorado', 'Pontuacao por possuir doutorado', 50, 0),
            ('Participacao em Projetos de Pesquisa', 'projetos_pesquisa', '10 pontos por ano de trabalho, maximo 100 pontos', 10, 100),
            ('Participacao em Congressos/Feiras/Eventos', 'congressos', 'Participacao em congressos, feiras, eventos e palestras', 2, 0),
            ('Resumo em Anais de Eventos', 'resumo_anais', 'Resumo publicado em anais de eventos', 2, 0),
            ('Artigo Completo em Anais de Eventos', 'artigo_completo_anais', 'Artigo completo publicado em anais de eventos', 4, 0),
            ('Artigo Cientifico Nacional', 'artigo_nacional', 'Artigo cientifico ou capitulo de livro nacional publicado', 10, 0),
            ('Artigo Cientifico Internacional', 'artigo_internacional', 'Artigo cientifico ou capitulo de livro internacional publicado', 15, 0),
            ('Livro/Patente', 'livro_patente', 'Livro publicado na area de interesse ou patente registrada', 20, 0),
            ('Participacao em Minicurso', 'minicurso', 'Participacao em minicurso (ate 4 horas) na area de interesse', 2, 0),
            ('Treinamento', 'treinamento', 'Treinamento (acima de 4 horas) na area de interesse', 5, 0),
        ]
        criterios = []
        for nome, tipo_criterio, desc, peso, peso_maximo in dados:
            c = CriterioClassificacao.objects.create(
                nome=nome,
                tipo_criterio=tipo_criterio,
                descricao=desc,
                peso=peso or 0,
                peso_maximo=peso_maximo,
                ativo=True,
                tenant=tenant,
            )
            criterios.append(c)
        return criterios

    def _criar_editais(self, tenant, admin):
        dados = [
            {
                'nome_edital': 'Bolsa de Iniciacao Cientifica',
                'area_estudo': 'Engenharia',
                'detalhes_edital': 'Programa de iniciacao cientifica para estudantes de graduacao.',
                'nome_instituto': 'ist_alimentos',
                'email_solicitante': f'admin@{tenant.dominio}.com.br',
                'telefone': '(67) 99999-0001',
                'endereco': 'Rua da Ciencia, 100 - Campo Grande/MS',
                'numero_vagas': 5,
                'modalidade_bolsa': 'nivel_1',
                'valor_total_bolsa': 6000.00,
                'valor_bolsa': 1200.00,
                'plataforma_tecnologica': 'Python, Django, Banco de Dados',
                'vigencia': 180,
                'qualificacao_minima': 'Graduação em Andamento',
                'conteudo_prova_teorica': 'Conhecimentos basicos em programacao.',
                'entrevista': 'Entrevista tecnica e comportamental.',
                'criterios_desempate': 'Maior nota na prova teorica.',
            },
            {
                'nome_edital': 'Bolsa de Mestrado',
                'area_estudo': 'Engenharia de Software',
                'detalhes_edital': 'Auxilio para alunos de mestrado em engenharia.',
                'nome_instituto': 'ist_construcao',
                'email_solicitante': f'admin@{tenant.dominio}.com.br',
                'telefone': '(67) 99999-0002',
                'endereco': 'Rua da Tecnologia, 200 - Campo Grande/MS',
                'numero_vagas': 3,
                'modalidade_bolsa': 'nivel_2',
                'valor_total_bolsa': 15000.00,
                'valor_bolsa': 5000.00,
                'plataforma_tecnologica': 'Machine Learning, Python, React',
                'vigencia': 365,
                'qualificacao_minima': 'Graduação Completa',
                'conteudo_prova_teorica': 'Conhecimentos avancados em ML e software.',
                'entrevista': 'Apresentacao de projeto de pesquisa.',
                'criterios_desempate': 'Experiencia profissional previa.',
            },
            {
                'nome_edital': 'Bolsa de Doutorado',
                'area_estudo': 'Inteligencia Artificial',
                'detalhes_edital': 'Auxilio para alunos de doutorado.',
                'nome_instituto': 'fatec_cg',
                'email_solicitante': f'admin@{tenant.dominio}.com.br',
                'telefone': '(67) 99999-0003',
                'endereco': 'Rua da Inovacao, 300 - Campo Grande/MS',
                'numero_vagas': 2,
                'modalidade_bolsa': 'nivel_3',
                'valor_total_bolsa': 18000.00,
                'valor_bolsa': 9000.00,
                'plataforma_tecnologica': 'Deep Learning, Python, TensorFlow',
                'vigencia': 730,
                'qualificacao_minima': 'Mestrado Concluído',
                'conteudo_prova_teorica': 'Conhecimentos avancados em IA e deep learning.',
                'entrevista': 'Defesa de projeto de tese.',
                'criterios_desempate': 'Publicacoes academicas previas.',
            },
        ]
        editais = []
        for d in dados:
            edital = EditalProvisorio.objects.create(
                criado_por=admin,
                tenant=tenant,
                status='aberto',
                **d,
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
