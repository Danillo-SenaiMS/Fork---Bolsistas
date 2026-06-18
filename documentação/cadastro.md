# Cadastro

App responsável pelo cadastro de bolsistas, formação acadêmica e solicitações de edição.

## Modelos

### `CadastroBolsista`
Dados do candidato a bolsista:
- `user` — OneToOne com `User`
- `endereco`, `data_nascimento` (>= 18 anos) — Dados pessoais
- `curriculo` — Upload de currículo (FileField)
- `foto` — Upload de foto (ImageField)
- Campos booleanos de critérios acadêmicos/profissionais:
  - `possui_graduacao`, `possui_mestrado`, `possui_doutorado`
  - `participacao_projetos_anos` — Anos de participação em projetos
  - `participacao_congressos`, `resumo_anais`, `artigo_completo_anais`
  - `artigo_cientifico_nacional`, `artigo_cientifico_internacional`
  - `livro_patente`, `participacao_minicurso`, `treinamento`
- `pontuacao_previa` — Pontuação calculada automaticamente
- `tenant` — FK para Tenant

### `CursoSuperior`
Cursos de graduação do bolsista:
- `bolsista` — FK para CadastroBolsista
- `instituicao`, `curso`, `grau` (tecnólogo/bacharelado/licenciatura)
- `ano_conclusao`

### `PosGraduacao`
Pós-graduações do bolsista:
- `bolsista` — FK para CadastroBolsista
- `tipo` — Pós-graduação, MBA, Especialização, Mestrado, Doutorado, Pós-doutorado
- `instituicao`, `area`, `ano_conclusao`

### `SolicitacaoEdicao`
Solicitações de alteração de dados que requerem aprovação:
- `bolsista` — FK para CadastroBolsista
- `campo` — Nome do campo a ser editado
- `valor_original`, `valor_novo` — Valores antes/depois
- `status` — Pendente, Aprovado, Rejeitado
- `revisado_por` — FK para User (gestor que revisou)
- `data_revisao` — Data da revisão

## Views

### `CadastroCreateView`
Criação do cadastro de bolsista.

### `CadastroDetailView`
Visualização do cadastro. Suporta acesso por pk para gestores.

### `CadastroUpdateView`
Edição do cadastro pelo próprio bolsista.

### `CadastroListView`
Listagem de cadastros (gestores veem todos, comum vê apenas o seu).

### `curso_add` / `curso_remove`
Views baseadas em função (FBVs) para adicionar/remover cursos superiores via HTMX. Recalcula a pontuação automaticamente após cada alteração.

### `pos_add` / `pos_remove`
FBVs para adicionar/remover pós-graduações via HTMX. Também recalcula pontuação.

### `SolicitacaoMultiplaView`
Criação de solicitação de edição em lote.

### `SolicitacaoListView`
Listagem de solicitações.

### `SolicitacaoRevisarView`
Revisão de solicitação por gestor (aprovar/rejeitar).

### `AdminDashboardView`
Dashboard administrativo com estatísticas gerais.

## Utilitários

### `calcular_pontuacao_previa`
Função que calcula a pontuação do bolsista com base nos critérios de classificação ativos. Usa os campos booleanos e relacionamentos do cadastro para atribuir notas conforme os pesos definidos.

## URLs

| Path | View | Nome |
|------|------|------|
| `criar/` | CadastroCreateView | `cadastro_create` |
| (vazio) | CadastroDetailView | `cadastro_detail` |
| `<pk>/` | CadastroDetailView | `cadastro_detail_pk` |
| `<pk>/editar/` | CadastroUpdateView | `cadastro_update_pk` |
| `<pk>/curso/add/` | curso_add | `curso_add` |
| `<pk>/curso/<curso_pk>/remove/` | curso_remove | `curso_remove` |
| `<pk>/pos/add/` | pos_add | `pos_add` |
| `<pk>/pos/<pos_pk>/remove/` | pos_remove | `pos_remove` |
| `lista/` | CadastroListView | `cadastro_list` |
| `solicitar/` | SolicitacaoMultiplaView | `solicitacao_criar` |
| `solicitacoes/` | SolicitacaoListView | `solicitacao_list` |
| `solicitacoes/<pk>/revisar/` | SolicitacaoRevisarView | `solicitacao_revisar` |
| `admin/` | AdminDashboardView | `admin_dashboard` |

## Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `models.py` | CadastroBolsista, CursoSuperior, PosGraduacao, SolicitacaoEdicao |
| `views.py` | Views de CRUD, solicitações e dashboard |
| `urls.py` | Rotas da app |
| `utils.py` | `calcular_pontuacao_previa` |
