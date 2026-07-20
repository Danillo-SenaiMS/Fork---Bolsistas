# Graph Report - C:\Users\danillo.araujo\OneDrive - SESIMS\Projetos\Fork---Bolsistas  (2026-07-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 721 nodes · 1593 edges · 86 communities (38 shown, 48 thin omitted)
- Extraction: 72% EXTRACTED · 28% INFERRED · 0% AMBIGUOUS · INFERRED: 442 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4649a749`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- User
- EditalProvisorio
- painel_bolsistas/tasks.py
- SolicitacaoMultiplaView
- editais/models.py
- Views
- CriterioClassificacao
- painel_bolsistas/views.py
- Views
- CronogramaTests
- SalvarAvaliacoesLoteTests
- Notificacao
- Views
- Views
- Notifications
- Base
- sidebar.js
- CadastroDetailView
- GroupRequiredMixin
- CadastroSerieTests
- 0002_create_groups.py
- UserManager
- LoginRequiredMiddleware
- 0008_migrate_rascunho_status.py
- NotificationsConfig
- opencode.json
- AccountsConfig
- BaseConfig
- CadastroConfig
- 0003_cadastro_numero_serie.py
- ClassificacaoConfig
- read_secret
- EditaisConfig
- 0002_numero_serie_data_evento_inscricao.py
- main
- PainelBolsistasConfig
- accounts/migrations/0001_initial.py
- AGENTS.md
- 0002_formacaoacademica_instituicao.py
- classificacao/migrations/0001_initial.py
- 0002_avaliacaobolsista.py
- asgi.py
- wsgi.py
- stack-deploy.sh script
- entrypoint.sh
- entrypoint-celery.sh
- editais/migrations/0001_initial.py
- 0003_data_entrevista_aplicacao.py
- 0004_remove_cronogramaevento_data_referencia_and_more.py
- 0005_remove_editalprovisorio_entrevista_and_more.py
- 0006_editalprovisorio_comentarios.py
- 0007_add_responsavel_field.py
- 0009_aplicacaoedital_nota_entrevista_and_more.py
- 0010_aplicacaoeditallog.py
- notifications/migrations/0001_initial.py
- AppConfig
- BaseCommand
- CreateView
- DetailView
- FormView
- ListView
- LoginRequiredMixin
- TemplateView
- TestCase
- UpdateView
- UserPassesTestMixin
- View

## God Nodes (most connected - your core abstractions)
1. `User` - 65 edges
2. `EditalProvisorio` - 55 edges
3. `CadastroBolsista` - 54 edges
4. `ManagerRequiredMixin` - 47 edges
5. `ManagerOrExecuteRequiredMixin` - 43 edges
6. `AplicacaoEdital` - 42 edges
7. `FormacaoAcademica` - 41 edges
8. `ViewUserRequiredMixin` - 33 edges
9. `Perfil` - 32 edges
10. `ExperienciaProfissional` - 31 edges

## Surprising Connections (you probably didn't know these)
- `Meta` --uses--> `User`  [INFERRED]
  notifications/models.py → accounts/models.py
- `CadastroDetailViewTests` --uses--> `User`  [INFERRED]
  cadastro/tests_cadastro_detail.py → accounts/models.py
- `CadastroSerieTests` --uses--> `User`  [INFERRED]
  cadastro/tests.py → accounts/models.py
- `SolicitacaoMultiplaFlowTests` --uses--> `User`  [INFERRED]
  cadastro/tests_solicitacao_flow.py → accounts/models.py
- `CadastroDetailView` --uses--> `User`  [INFERRED]
  cadastro/views.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (86 total, 48 thin omitted)

### Community 0 - "User"
Cohesion: 0.06
Nodes (60): AbstractUser, PerfilInline, UserAdmin, DocumentoExterno, Meta, Perfil, User, AprovarUsuarioView (+52 more)

### Community 1 - "EditalProvisorio"
Cohesion: 0.05
Nodes (48): ManagerOrExecuteRequiredMixin, ViewUserRequiredMixin, BaseInlineFormSet, DeleteView, AplicacaoEditalAdmin, CronogramaEventoInline, EditalProvisorioAdmin, AvaliacaoIndividualForm (+40 more)

### Community 2 - "painel_bolsistas/tasks.py"
Cohesion: 0.06
Nodes (51): gerar_json(), get_provider(), _groq_json(), _parse_json(), Retorna o provedor de IA ativo ('groq' ou None)., Tenta extrair JSON de uma resposta que pode vir envolta em markdown., GROQ expoe uma API compativel com OpenAI: reaproveita o SDK openai com base_url, Gera uma resposta em JSON usando o provedor configurado (GROQ). (+43 more)

### Community 3 - "SolicitacaoMultiplaView"
Cohesion: 0.08
Nodes (19): _carregar(), get_areas(), get_cursos_por_area(), get_instituicoes(), get_todos_cursos(), _attach_messages(), TestCase, Usuario so quer incluir graduacao; experiencia vazia nao deve travar. (+11 more)

### Community 4 - "editais/models.py"
Cohesion: 0.13
Nodes (8): DiasUteisTests, TestCase, adicionar_dias_uteis(), _carregar_feriados(), dias_uteis_entre(), gerar_numero_serie(), proximo_dia_1_ou_15(), proximo_dia_util()

### Community 5 - "Views"
Cohesion: 0.07
Nodes (26): `AlterarStatusAplicacaoView`, `AplicacaoEdital`, `AplicacaoListView`, `AplicarEditalView`, Arquivos Principais, `br_filters`, `CancelarAplicacaoView`, Constantes (+18 more)

### Community 6 - "CriterioClassificacao"
Cohesion: 0.13
Nodes (13): CriterioClassificacaoAdmin, AvaliacaoBolsista, CriterioClassificacao, Meta, AvaliacaoDetailView, AvaliacaoListView, CriterioCreateView, CriterioListView (+5 more)

### Community 7 - "painel_bolsistas/views.py"
Cohesion: 0.15
Nodes (13): analisar_bolsista(), painel_task_status(), PainelBolsistaDetailView, PainelBolsistasListView, _pode_usar_ia(), DetailView, ListView, Pagina 'Trilha do Bolsista' — historico completo de cada candidato:     aplicac (+5 more)

### Community 8 - "Views"
Cohesion: 0.11
Nodes (18): `AdminDashboardView`, Arquivos Principais, `BolsistaCreateView`, Cadastro, `CadastroBolsista`, `CadastroCreateView`, `CadastroDetailView`, `CadastroListView` (+10 more)

### Community 9 - "CronogramaTests"
Cohesion: 0.12
Nodes (4): CronogramaTests, InscricaoTests, NumeroSerieTests, TestCase

### Community 11 - "Notificacao"
Cohesion: 0.16
Nodes (9): Meta, Notificacao, MarcarLidaView, MarcarTodasLidasView, NotificacaoListView, ListView, LoginRequiredMixin, TemplateView (+1 more)

### Community 12 - "Views"
Cohesion: 0.13
Nodes (14): Arquivos Principais, `Classificacao`, `ClassificacaoCreateView`, `ClassificacaoCriterio`, `ClassificacaoDetailView`, `ClassificacaoListView`, Classificação, `CriterioClassificacao` (+6 more)

### Community 13 - "Views"
Cohesion: 0.14
Nodes (13): Accounts, `AprovarUsuarioView`, Arquivos Principais, `CustomLoginView`, `DocumentoExterno`, `HomeView`, `LandingPageView`, Modelos (+5 more)

### Community 14 - "Notifications"
Cohesion: 0.14
Nodes (13): Arquivos Principais, `MarcarLidaView`, `MarcarTodasLidasView`, Modelos, `Notificacao`, `NotificacaoListView`, `notificar_cadastro`, `notificar_classificacao` (+5 more)

### Community 15 - "Base"
Cohesion: 0.17
Nodes (12): `AdminRequiredMixin`, Arquivos Principais, Base, `DataModel`, `LoginRequiredMiddleware`, `ManagerRequiredMixin`, `media_protegida`, Middleware (+4 more)

### Community 16 - "sidebar.js"
Cohesion: 0.51
Nodes (10): applyState(), closeMobileSidebar(), getOverlay(), getSidebar(), getToggleBtn(), getWrapper(), init(), isCollapsed() (+2 more)

### Community 17 - "CadastroDetailView"
Cohesion: 0.31
Nodes (5): CadastroDetailViewTests, TestCase, CadastroDetailView, DetailView, LoginRequiredMixin

### Community 18 - "GroupRequiredMixin"
Cohesion: 0.40
Nodes (4): ExecuteUserRequiredMixin, GroupRequiredMixin, UserPassesTestMixin, user_has_group()

### Community 25 - "opencode.json"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

## Knowledge Gaps
- **97 isolated node(s):** `graphify`, ``User``, ``Perfil``, ``DocumentoExterno``, ``LandingPageView`` (+92 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **48 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `EditalProvisorio`, `SolicitacaoMultiplaView`, `editais/models.py`, `CriterioClassificacao`, `CronogramaTests`, `SalvarAvaliacoesLoteTests`, `Notificacao`, `CadastroDetailView`, `CadastroSerieTests`?**
  _High betweenness centrality (0.111) - this node is a cross-community bridge._
- **Why does `EditalProvisorio` connect `EditalProvisorio` to `User`, `painel_bolsistas/tasks.py`, `editais/models.py`, `painel_bolsistas/views.py`, `CronogramaTests`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Why does `CadastroBolsista` connect `User` to `EditalProvisorio`, `painel_bolsistas/tasks.py`, `SolicitacaoMultiplaView`, `editais/models.py`, `painel_bolsistas/views.py`, `CronogramaTests`, `CadastroDetailView`, `CadastroSerieTests`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **Are the 49 inferred relationships involving `User` (e.g. with `PerfilInline` and `UserAdmin`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `EditalProvisorio` (e.g. with `AplicacaoEditalAdmin` and `CronogramaEventoInline`) actually correct?**
  _`EditalProvisorio` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `CadastroBolsista` (e.g. with `AnexoComprobatorioInline` and `CadastroBolsistaAdmin`) actually correct?**
  _`CadastroBolsista` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `ManagerRequiredMixin` (e.g. with `AprovarUsuarioView` and `CustomLoginView`) actually correct?**
  _`ManagerRequiredMixin` has 41 INFERRED edges - model-reasoned connections that need verification._