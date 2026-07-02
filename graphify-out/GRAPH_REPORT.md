# Graph Report - Bolsas Senai  (2026-07-02)

## Corpus Check
- 98 files · ~36,323 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 680 nodes · 1348 edges · 74 communities (57 shown, 17 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 319 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce12c12b`
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
- [[_COMMUNITY_Community 55|Community 55]]
- [[_COMMUNITY_Community 56|Community 56]]
- [[_COMMUNITY_Community 64|Community 64]]
- [[_COMMUNITY_Community 65|Community 65]]
- [[_COMMUNITY_Community 66|Community 66]]
- [[_COMMUNITY_Community 67|Community 67]]
- [[_COMMUNITY_Community 68|Community 68]]
- [[_COMMUNITY_Community 70|Community 70]]

## God Nodes (most connected - your core abstractions)
1. `User` - 53 edges
2. `ManagerRequiredMixin` - 46 edges
3. `ManagerOrExecuteRequiredMixin` - 38 edges
4. `EditalProvisorio` - 35 edges
5. `Perfil` - 33 edges
6. `CadastroBolsista` - 32 edges
7. `ViewUserRequiredMixin` - 29 edges
8. `Command` - 25 edges
9. `FormacaoAcademica` - 24 edges
10. `SolicitacaoEdicao` - 24 edges

## Surprising Connections (you probably didn't know these)
- `Meta` --uses--> `User`  [INFERRED]
  editais/models.py → accounts/models.py
- `Meta` --uses--> `User`  [INFERRED]
  cadastro/models.py → accounts/models.py
- `SolicitacaoMultiplaView` --uses--> `User`  [INFERRED]
  cadastro/views.py → accounts/models.py
- `AvaliacaoBolsista` --uses--> `User`  [INFERRED]
  classificacao/models.py → accounts/models.py
- `CriterioClassificacao` --uses--> `User`  [INFERRED]
  classificacao/models.py → accounts/models.py

## Import Cycles
- None detected.

## Communities (74 total, 17 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (26): ManagerOrExecuteRequiredMixin, ViewUserRequiredMixin, DeleteView, EditalProvisorioForm, AplicacaoEdital, AlterarStatusAplicacaoView, analisar_edital(), AplicacaoListView (+18 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (49): AbstractUser, PerfilInline, UserAdmin, DocumentoExterno, Meta, Perfil, User, AprovarUsuarioView (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (10): calcular_pontuacao_previa(), _check_cadastro_permission(), _experiencia_formset_factory(), formacao_add(), formacao_remove(), _is_manager(), _recalcular_pontuacao(), _salvar_anexos() (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.04
Nodes (48): accounts/models.py — User + Perfil + DocumentoExterno, Atividades, Atividades, Atividades, Atividades, Atividades, Atividades, Atividades (+40 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (16): BaseInlineFormSet, CronogramaEventoInline, DistribuicaoBolsaInline, EditalProvisorioAdmin, BaseCronogramaFormSet, BaseDistribuicaoFormSet, CronogramaEventoForm, DistribuicaoBolsaForm (+8 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (28): `AlterarStatusAplicacaoView`, `AplicacaoEdital`, `AplicacaoListView`, `AplicarEditalView`, Arquivos Principais, `br_filters`, `CancelarAplicacaoView`, Constantes (+20 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (18): `AdminDashboardView`, Arquivos Principais, `BolsistaCreateView`, Cadastro, `CadastroBolsista`, `CadastroCreateView`, `CadastroDetailView`, `CadastroListView` (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (22): analisar_bolsista(), _analise_fallback(), _criterios_texto(), _editais_texto(), _normalizar_radar(), _normalizar_sugestoes(), _perfil_texto(), Monta uma descrição textual resumida do perfil do candidato. (+14 more)

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

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (5): BaseCommand, Command, _faixa_valores_nivel(), Sobrescreve created_at/updated_at espalhando nos ultimos N dias., Extrai os valores minimo e maximo de um nivel, considerando experiencia_valores.

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

### Community 43 - "Community 43"
Cohesion: 0.15
Nodes (14): DetailView, analisar_bolsista_task(), _notificar_conclusao(), resumir_bolsista_task(), sugerir_avaliacao_task(), analisar_bolsista(), painel_task_status(), PainelBolsistaDetailView (+6 more)

### Community 64 - "Community 64"
Cohesion: 0.13
Nodes (22): gerar_json(), get_provider(), _google_json(), _openai_json(), _parse_json(), Retorna o provedor de IA ativo ('openai', 'google' ou None)., Tenta extrair JSON de uma resposta que pode vir envolta em markdown., Gera uma resposta em JSON usando o provedor configurado. (+14 more)

### Community 66 - "Community 66"
Cohesion: 0.11
Nodes (15): ExecuteUserRequiredMixin, GroupRequiredMixin, user_has_group(), CriterioClassificacaoAdmin, AvaliacaoBolsista, CriterioClassificacao, AvaliacaoDetailView, AvaliacaoListView (+7 more)

## Knowledge Gaps
- **173 isolated node(s):** `$schema`, `plugin`, `Migration`, `Migration`, `Meta` (+168 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `User` connect `Community 1` to `Community 0`, `Community 2`, `Community 66`, `Community 4`, `Community 14`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `EditalProvisorio` connect `Community 4` to `Community 0`, `Community 1`, `Community 43`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `Command` connect `Community 14` to `Community 1`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Are the 41 inferred relationships involving `User` (e.g. with `PerfilInline` and `UserAdmin`) actually correct?**
  _`User` has 41 INFERRED edges - model-reasoned connections that need verification._
- **Are the 39 inferred relationships involving `ManagerRequiredMixin` (e.g. with `AprovarUsuarioView` and `CustomLoginView`) actually correct?**
  _`ManagerRequiredMixin` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `ManagerOrExecuteRequiredMixin` (e.g. with `BolsistaCreateForm` and `BolsistaCreateView`) actually correct?**
  _`ManagerOrExecuteRequiredMixin` has 32 INFERRED edges - model-reasoned connections that need verification._
- **Are the 20 inferred relationships involving `EditalProvisorio` (e.g. with `CronogramaEventoInline` and `DistribuicaoBolsaInline`) actually correct?**
  _`EditalProvisorio` has 20 INFERRED edges - model-reasoned connections that need verification._