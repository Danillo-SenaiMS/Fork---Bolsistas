from django.core.management.base import BaseCommand
from faker import Faker

from accounts.models import User, Perfil, Tenant
from cadastro.models import CadastroBolsista, FormacaoAcademica
from editais.models import EditalProvisorio, AplicacaoEdital
from classificacao.models import CriterioClassificacao, Classificacao, ClassificacaoCriterio

fake = Faker('pt_BR')


class Command(BaseCommand):
    help = 'Gera dados fake adicionais para o Painel de Bolsistas'

    def handle(self, *args, **options):
        self.stdout.write('Gerando dados para o Painel de Bolsistas...')

        tenants = Tenant.objects.all()
        if not tenants.exists():
            sesi = Tenant.objects.create(nome='SESI', dominio='sesi', ativo=True)
            senai = Tenant.objects.create(nome='SENAI', dominio='senai', ativo=True)
            tenants = [sesi, senai]
            self.stdout.write('  Tenants criados: SESI, SENAI')

        for tenant in tenants:
            self._criar_bolsistas(tenant)

        self.stdout.write(self.style.SUCCESS('Seed do painel concluido!'))
        self.stdout.write('  Total bolsistas: {}'.format(CadastroBolsista.objects.count()))
        self.stdout.write('  Total formacoes: {}'.format(FormacaoAcademica.objects.count()))
        self.stdout.write('  Total editais: {}'.format(EditalProvisorio.objects.count()))

    def _criar_bolsistas(self, tenant):
        self.stdout.write(f'  Populando tenant: {tenant.nome}...')

        for i in range(8):
            primeiro = fake.first_name()
            sobrenome = fake.last_name()
            email = f'{primeiro.lower()}.{sobrenome.lower()}@{tenant.dominio}.com.br'

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'nome_completo': f'{primeiro} {sobrenome}',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('123456')
                user.save()

            if not hasattr(user, 'perfil') or not user.perfil:
                Perfil.objects.get_or_create(
                    user=user,
                    defaults={
                        'tipo': 'COMMON',
                        'tenant': tenant,
                    }
                )

            if hasattr(user, 'cadastro') and user.cadastro:
                continue

            cad = CadastroBolsista.objects.create(
                user=user,
                telefone=fake.phone_number(),
                data_nascimento=fake.date_of_birth(minimum_age=18, maximum_age=65),
                rua=fake.street_name(),
                numero=str(fake.building_number()),
                bairro=fake.bairro(),
                cidade=fake.city(),
                estado=fake.random_element(['MS', 'SP', 'PR', 'RJ', 'RS']),
                tenant=tenant,
            )

            tipos = ['ensino_medio', 'graduacao', 'especializacao', 'mestrado', 'doutorado']
            for idx, tipo in enumerate(tipos):
                if fake.boolean(chance_of_getting_true=70 - idx * 15):
                    FormacaoAcademica.objects.create(
                        bolsista=cad,
                        tipo=tipo,
                        status=fake.random_element(['', 'em_andamento', 'concluida']),
                        instituicao=fake.company(),
                        curso=fake.random_element([
                            'Engenharia de Producao', 'Administracao',
                            'Ciencia da Computacao', 'Direito',
                            'Engenharia Mecanica', 'Biomedicina',
                            'Fisica', 'Quimica', 'Matematica',
                            'Engenharia Eletrica', 'Psicologia',
                        ]),
                        area=fake.random_element([
                            'Inteligencia Artificial', 'Automacao Industrial',
                            'Energias Renovaveis', 'Biotecnologia',
                            'Materiais Avancados', 'Robotica',
                            'Data Science', 'Gestao de Projetos',
                        ]),
                        ano_conclusao=fake.random_int(min=2005, max=2026),
                        tenant=tenant,
                    )

            cad.participacao_projetos_anos = fake.random_int(min=0, max=12) if fake.boolean(chance_of_getting_true=50) else 0
            cad.participacao_congressos = fake.boolean(chance_of_getting_true=40)
            cad.resumo_anais = fake.boolean(chance_of_getting_true=30)
            cad.artigo_completo_anais = fake.boolean(chance_of_getting_true=25)
            cad.artigo_cientifico_nacional = fake.boolean(chance_of_getting_true=20)
            cad.artigo_cientifico_internacional = fake.boolean(chance_of_getting_true=15)
            cad.livro_patente = fake.boolean(chance_of_getting_true=10)
            cad.participacao_minicurso = fake.boolean(chance_of_getting_true=35)
            cad.treinamento = fake.boolean(chance_of_getting_true=30)
            cad.save()

            self._criar_editais_e_aplicacoes(cad, tenant)

    def _criar_editais_e_aplicacoes(self, cad, tenant):
        if EditalProvisorio.objects.filter(tenant=tenant, status='aberto').count() >= 3:
            return

        admin = User.objects.filter(
            perfil__tipo='ADMIN',
            perfil__tenant=tenant,
        ).first()

        if not admin:
            email_admin = f'admin@{tenant.dominio}.com.br'
            admin = User.objects.filter(email=email_admin).first()
            if not admin:
                admin = User.objects.create_user(
                    email=email_admin,
                    nome_completo=f'Admin {tenant.nome}',
                    password='123456',
                )
                admin.is_active = True
                admin.save()
                Perfil.objects.create(user=admin, tipo='ADMIN', tenant=tenant)

        editais_config = [
            {
                'nome_edital': 'Bolsa de Iniciacao Cientifica 2026',
                'area_estudo': fake.random_element(['Engenharia', 'Tecnologia', 'Ciencias Exatas']),
                'detalhes_edital': 'Programa de iniciacao cientifica para estudantes.',
                'nome_instituto': 'ist_alimentos',
                'email_solicitante': admin.email,
                'telefone': '(67) 99999-0001',
                'endereco': 'Rua da Ciencia, 100 - Campo Grande/MS',
                'numero_vagas': 5,
                'modalidade_bolsa': 'nivel_1',
                'valor_total_bolsa': 6000.00,
                'valor_bolsa': 1200.00,
                'plataforma_tecnologica': 'Python, Django, Banco de Dados',
                'vigencia': 180,
                'qualificacao_minima': 'Graduacao em Andamento',
                'conteudo_prova_teorica': 'Conhecimentos basicos em programacao e banco de dados.',
                'entrevista': 'Entrevista tecnica e comportamental.',
                'criterios_desempate': 'Maior nota na prova teorica.',
            },
            {
                'nome_edital': 'Bolsa de Mestrado em Tecnologia',
                'area_estudo': 'Engenharia de Software',
                'detalhes_edital': 'Auxilio para alunos de mestrado.',
                'nome_instituto': 'ist_construcao',
                'email_solicitante': admin.email,
                'telefone': '(67) 99999-0002',
                'endereco': 'Rua da Tecnologia, 200 - Campo Grande/MS',
                'numero_vagas': 3,
                'modalidade_bolsa': 'nivel_2',
                'valor_total_bolsa': 15000.00,
                'valor_bolsa': 5000.00,
                'plataforma_tecnologica': 'Machine Learning, Python, React',
                'vigencia': 365,
                'qualificacao_minima': 'Graduacao Completa',
                'conteudo_prova_teorica': 'Conhecimentos avancados em ML e engenharia de software.',
                'entrevista': 'Apresentacao de projeto de pesquisa.',
                'criterios_desempate': 'Experiencia profissional previa e publicacoes.',
            },
            {
                'nome_edital': 'Bolsa de Doutorado em IA',
                'area_estudo': 'Inteligencia Artificial',
                'detalhes_edital': 'Auxilio para alunos de doutorado na area de IA.',
                'nome_instituto': 'fatec_cg',
                'email_solicitante': admin.email,
                'telefone': '(67) 99999-0003',
                'endereco': 'Rua da Inovacao, 300 - Campo Grande/MS',
                'numero_vagas': 2,
                'modalidade_bolsa': 'nivel_3',
                'valor_total_bolsa': 18000.00,
                'valor_bolsa': 9000.00,
                'plataforma_tecnologica': 'Deep Learning, Python, TensorFlow',
                'vigencia': 730,
                'qualificacao_minima': 'Mestrado Concluido',
                'conteudo_prova_teorica': 'Conhecimentos avancados em IA e deep learning.',
                'entrevista': 'Defesa de projeto de tese.',
                'criterios_desempate': 'Publicacoes academicas previas.',
            },
        ]

        for cfg in editais_config:
            if not EditalProvisorio.objects.filter(tenant=tenant, nome_edital=cfg['nome_edital']).exists():
                EditalProvisorio.objects.create(
                    criado_por=admin,
                    tenant=tenant,
                    status='aberto',
                    **cfg,
                )
