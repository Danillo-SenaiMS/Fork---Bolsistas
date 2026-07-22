# Graph Report - Fork---Bolsistas  (2026-07-22)

## Corpus Check
- 124 files · ~52,489 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 734 nodes · 1618 edges · 79 communities (42 shown, 37 thin omitted)
- Extraction: 73% EXTRACTED · 27% INFERRED · 0% AMBIGUOUS · INFERRED: 442 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a0ff2879`
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
- users.md
- FormView
- README.md

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
- `AvaliacaoBolsista` --uses--> `User`  [INFERRED]
  classificacao/models.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (79 total, 37 thin omitted)

### Community 0 - "User"
Cohesion: 0.06
Nodes (57): AbstractUser, PerfilInline, UserAdmin, Perfil, User, AnexoComprobatorioInline, CadastroBolsistaAdmin, ExperienciaProfissionalInline (+49 more)

### Community 1 - "EditalProvisorio"
Cohesion: 0.14
Nodes (11): BaseInlineFormSet, AplicacaoEditalAdmin, CronogramaEventoInline, EditalProvisorioAdmin, AvaliacaoIndividualForm, BaseCronogramaFormSet, CronogramaEventoForm, Meta (+3 more)

### Community 2 - "painel_bolsistas/tasks.py"
Cohesion: 0.06
Nodes (51): gerar_json(), get_provider(), _groq_json(), _parse_json(), Retorna o provedor de IA ativo ('groq' ou None)., Tenta extrair JSON de uma resposta que pode vir envolta em markdown., GROQ expoe uma API compativel com OpenAI: reaproveita o SDK openai com base_url, Gera uma resposta em JSON usando o provedor configurado (GROQ). (+43 more)

### Community 3 - "SolicitacaoMultiplaView"
Cohesion: 0.27
Nodes (4): _attach_messages(), TestCase, Usuario so quer incluir graduacao; experiencia vazia nao deve travar., SolicitacaoMultiplaFlowTests

### Community 4 - "editais/models.py"
Cohesion: 0.13
Nodes (8): DiasUteisTests, TestCase, adicionar_dias_uteis(), _carregar_feriados(), dias_uteis_entre(), gerar_numero_serie(), proximo_dia_1_ou_15(), proximo_dia_util()

### Community 5 - "Views"
Cohesion: 0.07
Nodes (26): `AlterarStatusAplicacaoView`, `AplicacaoEdital`, `AplicacaoListView`, `AplicarEditalView`, Arquivos Principais, `br_filters`, `CancelarAplicacaoView`, Constantes (+18 more)

### Community 6 - "CriterioClassificacao"
Cohesion: 0.11
Nodes (23): ExecuteUserRequiredMixin, GroupRequiredMixin, ManagerOrExecuteRequiredMixin, ManagerRequiredMixin, UserPassesTestMixin, user_has_group(), ViewUserRequiredMixin, AvaliacaoBolsista (+15 more)

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
Cohesion: 0.07
Nodes (21): DocumentoExterno, Meta, UserManager, DataModel, Meta, health_check(), media_protegida(), Endpoint simples para health checks do load balancer/monitoramento. (+13 more)

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

### Community 18 - "GroupRequiredMixin"
Cohesion: 0.12
Nodes (11): AprovarUsuarioView, CustomLoginView, HomeView, LandingPageView, Meta, FormView, LoginRequiredMixin, TemplateView (+3 more)

### Community 21 - "UserManager"
Cohesion: 0.17
Nodes (9): EditalProvisorio, analisar_edital(), edital_task_status(), minha_compatibilidade(), Retorna resumo IA do edital + % de compatibilidade do ViewUser logado., _render_edital_result(), resumir_edital(), _task_running_partial() (+1 more)

### Community 25 - "opencode.json"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

### Community 58 - "AppConfig"
Cohesion: 0.24
Nodes (5): AplicacaoEditalListView, AplicacaoListView, EditalProvisorioListView, ListView, LoginRequiredMixin

### Community 62 - "BaseCommand"
Cohesion: 0.20
Nodes (4): DeleteView, EditalProvisorioForm, EditalProvisorioDeleteView, UserPassesTestMixin

### Community 68 - "CreateView"
Cohesion: 0.18
Nodes (5): ContextMixin, EditalProvisorioCreateView, EditalProvisorioUpdateView, CreateView, UpdateView

### Community 70 - "DetailView"
Cohesion: 0.29
Nodes (6): AplicacaoEditalLog, _calcular_status(), EditarAvaliacaoView, View, _registrar_log(), SalvarAvaliacoesLoteView

### Community 71 - "users.md"
Cohesion: 0.13
Nodes (14): Apagar tudo (containers + volumes + dados), Comandos dos containers Docker, Executar comandos Django dentro do container, Parar sem perder dados (volumes preservados), Parar todos os containers, Permissões por grupo, Recriar containers (após mudanças no Dockerfile), Recuperação de senha (+6 more)

### Community 80 - "README.md"
Cohesion: 0.17
Nodes (11): Bolsas SENAI-MS, Comandos Uteis, Estrutura do Projeto, Funcionalidades, Grupos de Usuario, Pre-requisitos, Servicos Docker, Setup com Docker (recomendado) (+3 more)

## Knowledge Gaps
- **118 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `Migration`, `Migration`, `Meta` (+113 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **37 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `User` to `EditalProvisorio`, `SolicitacaoMultiplaView`, `editais/models.py`, `CriterioClassificacao`, `DetailView`, `CronogramaTests`, `SalvarAvaliacoesLoteTests`, `Notificacao`, `CadastroDetailView`, `GroupRequiredMixin`, `CadastroSerieTests`, `UserManager`?**
  _High betweenness centrality (0.107) - this node is a cross-community bridge._
- **Why does `EditalProvisorio` connect `UserManager` to `User`, `EditalProvisorio`, `painel_bolsistas/tasks.py`, `editais/models.py`, `CreateView`, `DetailView`, `CriterioClassificacao`, `painel_bolsistas/views.py`, `CronogramaTests`, `FormView`, `Notificacao`, `GroupRequiredMixin`, `AppConfig`, `BaseCommand`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Why does `CadastroBolsista` connect `User` to `painel_bolsistas/tasks.py`, `editais/models.py`, `DetailView`, `painel_bolsistas/views.py`, `CronogramaTests`, `Notificacao`, `GroupRequiredMixin`, `CadastroSerieTests`, `UserManager`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 49 inferred relationships involving `User` (e.g. with `PerfilInline` and `UserAdmin`) actually correct?**
  _`User` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 33 inferred relationships involving `EditalProvisorio` (e.g. with `AplicacaoEditalAdmin` and `CronogramaEventoInline`) actually correct?**
  _`EditalProvisorio` has 33 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `CadastroBolsista` (e.g. with `AnexoComprobatorioInline` and `CadastroBolsistaAdmin`) actually correct?**
  _`CadastroBolsista` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 41 inferred relationships involving `ManagerRequiredMixin` (e.g. with `AprovarUsuarioView` and `CustomLoginView`) actually correct?**
  _`ManagerRequiredMixin` has 41 INFERRED edges - model-reasoned connections that need verification._