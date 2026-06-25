# Graph Report - Bolsas Senai  (2026-06-25)

## Corpus Check
- 86 files · ~35,286 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 619 nodes · 1238 edges · 64 communities (53 shown, 11 thin omitted)
- Extraction: 71% EXTRACTED · 29% INFERRED · 0% AMBIGUOUS · INFERRED: 360 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7b22bf14`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 43|Community 43]]

## God Nodes (most connected - your core abstractions)
1. `ManagerRequiredMixin` - 59 edges
2. `User` - 53 edges
3. `EditalProvisorio` - 39 edges
4. `Perfil` - 32 edges
5. `CadastroBolsista` - 31 edges
6. `AplicacaoEdital` - 30 edges
7. `FormacaoAcademica` - 28 edges
8. `SolicitacaoEdicao` - 28 edges
9. `ExperienciaProfissional` - 26 edges
10. `AnexoComprobatorio` - 26 edges

## Surprising Connections (you probably didn't know these)
- `Meta` --uses--> `User`  [INFERRED]
  cadastro/models.py → accounts/models.py
- `Meta` --uses--> `User`  [INFERRED]
  classificacao/models.py → accounts/models.py
- `Meta` --uses--> `User`  [INFERRED]
  editais/models.py → accounts/models.py
- `Meta` --uses--> `User`  [INFERRED]
  notifications/models.py → accounts/models.py
- `AnexoComprobatorio` --uses--> `User`  [INFERRED]
  cadastro/models.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (64 total, 11 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (38): BaseInlineFormSet, DeleteView, DetailView, AplicacaoEditalAdmin, CronogramaEventoInline, DistribuicaoBolsaInline, EditalProvisorioAdmin, BaseCronogramaFormSet (+30 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (38): DataModel, Meta, AnexoComprobatorioAdmin, CadastroBolsistaAdmin, ExperienciaProfissionalAdmin, FormacaoAcademicaAdmin, SolicitacaoEdicaoAdmin, Migration (+30 more)

### Community 2 - "Community 2"
Cohesion: 0.09
Nodes (28): AdminRequiredMixin, ManagerRequiredMixin, RoleRequiredMixin, ClassificacaoAdmin, ClassificacaoCriterioAdmin, CriterioClassificacaoAdmin, Classificacao, ClassificacaoCriterio (+20 more)

### Community 3 - "Community 3"
Cohesion: 0.04
Nodes (48): accounts/models.py — User + Perfil + DocumentoExterno, Atividades, Atividades, Atividades, Atividades, Atividades, Atividades, Atividades (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.12
Nodes (19): AbstractUser, DocumentoExternoAdmin, PerfilAdmin, UserAdmin, DocumentoExterno, Meta, Perfil, User (+11 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (28): `AlterarStatusAplicacaoView`, `AplicacaoEdital`, `AplicacaoListView`, `AplicarEditalView`, Arquivos Principais, `br_filters`, `CancelarAplicacaoView`, Constantes (+20 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (17): `AdminDashboardView`, Arquivos Principais, Cadastro, `CadastroBolsista`, `CadastroCreateView`, `CadastroDetailView`, `CadastroListView`, `CadastroUpdateView` (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.16
Nodes (7): NotificacaoAdmin, Meta, Notificacao, MarcarLidaView, MarcarTodasLidasView, NotificacaoListView, View

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (8): AccountsConfig, AppConfig, BaseConfig, CadastroConfig, ClassificacaoConfig, EditaisConfig, NotificationsConfig, PainelBolsistasConfig

### Community 9 - "Community 9"
Cohesion: 0.13
Nodes (14): Arquivos Principais, `Classificacao`, `ClassificacaoCreateView`, `ClassificacaoCriterio`, `ClassificacaoDetailView`, `ClassificacaoListView`, Classificação, `CriterioClassificacao` (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (13): Accounts, `AprovarUsuarioView`, Arquivos Principais, `CustomLoginView`, `DocumentoExterno`, `HomeView`, `LandingPageView`, Modelos (+5 more)

### Community 11 - "Community 11"
Cohesion: 0.14
Nodes (13): Arquivos Principais, `MarcarLidaView`, `MarcarTodasLidasView`, Modelos, `Notificacao`, `NotificacaoListView`, `notificar_cadastro`, `notificar_classificacao` (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.15
Nodes (12): `AdminRequiredMixin`, Arquivos Principais, Base, `DataModel`, `LoginRequiredMiddleware`, `ManagerRequiredMixin`, `media_protegida`, Middleware (+4 more)

### Community 13 - "Community 13"
Cohesion: 0.26
Nodes (8): avaliar_candidato(), _build_candidato_context(), _build_edital_context(), _get_llm(), summarize_editais_lista(), summarize_edital(), SummarizeState, TypedDict

### Community 14 - "Community 14"
Cohesion: 0.30
Nodes (7): analisar_candidato(), _build_bolsista_context(), _build_editais_context(), gerar_resumo_bolsista(), _get_llm(), analisar_candidato_view(), gerar_resumo_view()

### Community 15 - "Community 15"
Cohesion: 0.47
Nodes (10): applyState(), closeMobileSidebar(), getOverlay(), getSidebar(), getToggleBtn(), getWrapper(), init(), isCollapsed() (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (7): Ambiente, Atividades, Configurações, Estrutura inicial, Objetivo, Padrões globais, 🟦 SPRINT 0 — SETUP E FUNDAÇÃO DO PROJETO

### Community 17 - "Community 17"
Cohesion: 0.29
Nodes (7): Atividades, Models, Objetivo, Regras, 🟦 SPRINT 3 — CADASTRO DE BOLSISTAS, Uploads, Views

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (7): Atividades, Lógica, Models, Notificação, Objetivo, Permissões, 🟦 SPRINT 6 — CLASSIFICAÇÃO

### Community 19 - "Community 19"
Cohesion: 0.29
Nodes (7): Atividades, Modelagem, Objetivo, Roles, Segurança, 🟦 SPRINT 1 — AUTENTICAÇÃO E USUÁRIOS, Views e fluxo

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (5): ✅ DEFINIÇÃO DE PRONTO (DoD), 📊 ORDEM DE PRIORIDADE CRÍTICA, 📌 PLANO DE DESENVOLVIMENTO EM SPRINTS — PORTAL DA INOVAÇÃO (DJANGO), ⚠️ RISCOS PRINCIPAIS, 🎯 VISÃO GERAL

### Community 21 - "Community 21"
Cohesion: 0.33
Nodes (6): Atividades, Objetivo, Permissões, Proteção de arquivos, Revisão de segurança, 🟦 SPRINT 2 — PERMISSÕES E SEGURANÇA

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (6): Atividades, Models, Objetivo, Permissões, 🟦 SPRINT 4 — EDITAIS, Views

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (6): Atividades, Fluxo, Models, Objetivo, 🟦 SPRINT 5 — APLICAÇÕES EM EDITAIS, Views

### Community 24 - "Community 24"
Cohesion: 0.33
Nodes (6): Atividades, Estilo, Interatividade, Layout, Objetivo, 🟦 SPRINT 9 — UI/UX E FRONTEND

### Community 25 - "Community 25"
Cohesion: 0.33
Nodes (6): Atividades, Configuração, Objetivo, Performance, Segurança, 🟦 SPRINT 10 — HARDENING E FINALIZAÇÃO

### Community 26 - "Community 26"
Cohesion: 0.40
Nodes (5): Atividades, Funcionalidades, Objetivo, Setup, 🟦 SPRINT 7 — NOTIFICAÇÕES (CELERY)

### Community 27 - "Community 27"
Cohesion: 0.40
Nodes (5): Atividades, Funcionalidades, Objetivo, 🟦 SPRINT 8 — DASHBOARD, UI

## Knowledge Gaps
- **168 isolated node(s):** `$schema`, `plugin`, `Migration`, `Meta`, `Meta` (+163 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ManagerRequiredMixin` connect `Community 2` to `Community 0`, `Community 1`, `Community 4`, `Community 14`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `User` connect `Community 4` to `Community 0`, `Community 1`, `Community 2`, `Community 7`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `EditalProvisorio` connect `Community 0` to `Community 1`, `Community 4`, `Community 14`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 52 inferred relationships involving `ManagerRequiredMixin` (e.g. with `AprovarUsuarioView` and `CustomLoginView`) actually correct?**
  _`ManagerRequiredMixin` has 52 INFERRED edges - model-reasoned connections that need verification._
- **Are the 42 inferred relationships involving `User` (e.g. with `DocumentoExternoAdmin` and `PerfilAdmin`) actually correct?**
  _`User` has 42 INFERRED edges - model-reasoned connections that need verification._
- **Are the 27 inferred relationships involving `EditalProvisorio` (e.g. with `AplicacaoEditalAdmin` and `CronogramaEventoInline`) actually correct?**
  _`EditalProvisorio` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 25 inferred relationships involving `Perfil` (e.g. with `DocumentoExternoAdmin` and `PerfilAdmin`) actually correct?**
  _`Perfil` has 25 INFERRED edges - model-reasoned connections that need verification._