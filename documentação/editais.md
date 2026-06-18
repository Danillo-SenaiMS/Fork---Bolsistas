# Editais

App responsável pela criação e gestão completa de editais (antigo edital provisório), incluindo cronograma, distribuição de bolsas e candidaturas.

## Constantes

### `NIVEL_BOLSA_CONFIG`
Dicionário que define 4 níveis de bolsa com suas qualificações, experiências e faixas de valor:
- **Nível 1**: Ensino Médio/Técnico/Graduação em Andamento — R$ 500 a R$ 2.000
- **Nível 2**: Graduação Completa/Tecnólogo — R$ 2.500 a R$ 10.000
- **Nível 3**: Mestrado — R$ 4.500 a R$ 12.000
- **Nível 4**: Doutorado — R$ 6.500 a R$ 14.000

## Modelos

### `EditalProvisorio`
Modelo principal do edital com estrutura completa:
- **Dados do Edital**: `nome_edital`, `area_estudo`, `detalhes_edital`
- **Instituto**: `nome_instituto` (7 opções: ISI Biomassa, IST Alimentos, IST Construção, FATEC CG, DR), `email_solicitante`, `telefone`, `endereco`
- **Configuração da Bolsa**: `numero_vagas`, `modalidade_bolsa` (4 níveis), `valor_total_bolsa`, `valor_bolsa`, `valor_minimo`, `valor_maximo`, `modalidade_atuacao` (presencial/remota), `plataforma_tecnologica`, `vigencia` (dias, 15-1095), `endereco_atuacao`
- **Requisitos**: `qualificacao_minima`, `detalhes_qualificacao_minima`, `conhecimento_desejavel`, `conteudo_prova_teorica`, `entrevista`, `criterios_desempate`
- **Status**: Aberto, Encerrado, Em Análise, Cancelado
- **Metadados**: `criado_por` (FK User), `tenant` (FK Tenant)

Propriedades computadas:
- `total_eventos` — Quantidade de eventos no cronograma
- `total_distribuido` — Soma de quantidade × valor unitário de todas as distribuições
- `total_vagas_distribuidas` — Soma de quantidades de todas as distribuições

### `CronogramaEvento`
Eventos do cronograma do edital:
- `edital` — FK para EditalProvisorio
- `evento` — 9 tipos (início submissão, limite submissão, resultado aptas, prova teórica, resultado prova, envio documentação, entrevista, resultado final, outorga)
- `data_referencia` — Descrição da data (texto livre)
- `observacao`, `ordem`

### `DistribuicaoBolsa`
Distribuição de vagas por nível de experiência:
- `edital` — FK para EditalProvisorio
- `experiencia` — Nível de experiência
- `quantidade` — Número de bolsistas
- `valor_unitario` — Valor por bolsista

Propriedade computada: `subtotal` = quantidade × valor_unitario

### `AplicacaoEdital`
Candidatura de um bolsista a um edital:
- `bolsista` — FK para CadastroBolsista
- `edital` — FK para EditalProvisorio
- `status` — Pendente, Em Análise, Aprovado, Rejeitado
- `data_aplicacao` — Data/hora automática
- `unique_together` = (bolsista, edital) — Um bolsista só pode se candidatar uma vez

## Views

### `EditalProvisorioListView`
Listagem paginada com busca por instituto e filtro por status. Superusuários veem todos os tenants.

### `EditalProvisorioCreateView`
Criação com formulário principal + formsets inline de Cronograma e Distribuição. Validações:
- Soma da distribuição não pode exceder `valor_total_bolsa`
- Valor unitário deve estar dentro da faixa do nível
- Vigência entre 15 e 1095 dias
- Endereço de atuação obrigatório para modalidade remota

### `EditalProvisorioUpdateView`
Edição com os mesmos formsets e validações da criação.

### `EditalProvisorioDetailView`
Visualização completa com todas as seções, cronograma (timeline visual) e distribuição de bolsistas (tabela com subtotais).

### `EditalProvisorioDeleteView`
Exclusão com tela de confirmação.

### `edital_pdf_view`
Geração de PDF do edital usando xhtml2pdf (pisa).

### `AplicarEditalView`
Candidatura de bolsista a um edital. Dispara classificação automática baseada nos critérios ativos.

### `AplicacaoListView`
Listagem de candidaturas. Gestores veem todas com filtro por status; bolsistas veem apenas suas próprias.

### `CancelarAplicacaoView`
Cancelamento de candidatura pendente.

### `AlterarStatusAplicacaoView`
Alteração de status por gestor. Suporta HTMX para atualização inline.

## Forms

### `EditalProvisorioForm`
Formulário principal com 19 campos. Atualiza dinamicamente as opções de `qualificacao_minima` conforme a `modalidade_bolsa` selecionada. Define `valor_minimo`/`valor_maximo` automaticamente pelo `NIVEL_BOLSA_CONFIG`.

### `DistribuicaoBolsaForm`
Valida que:
- Experiência deve ser selecionada se quantidade/valor preenchidos
- Valor unitário dentro da faixa do nível e experiência

### `CronogramaEventoForm`
Valida que evento e data de referência sejam preenchidos juntos.

### Formsets
- `DistribuicaoBolsaFormSet` — Valida que a soma total não excede o orçamento e propaga o tenant
- `CronogramaEventoFormSet` — Propaga o tenant para novos registros

## Template Tags

### `br_filters`
- `br_money` — Formata valor numérico como moeda brasileira (R$ 1.234,56)

## URLs

| Path | View | Nome |
|------|------|------|
| `/` | EditalProvisorioListView | `edital_list` |
| `criar/` | EditalProvisorioCreateView | `edital_create` |
| `<pk>/` | EditalProvisorioDetailView | `edital_detail` |
| `<pk>/pdf/` | edital_pdf_view | `edital_pdf` |
| `<pk>/editar/` | EditalProvisorioUpdateView | `edital_update` |
| `<pk>/excluir/` | EditalProvisorioDeleteView | `edital_delete` |
| `<pk>/aplicar/` | AplicarEditalView | `aplicar_edital` |
| `aplicacoes/` | AplicacaoListView | `aplicacao_list` |
| `aplicacoes/<pk>/cancelar/` | CancelarAplicacaoView | `cancelar_aplicacao` |
| `aplicacoes/<pk>/status/` | AlterarStatusAplicacaoView | `alterar_status_aplicacao` |

## Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `models.py` | EditalProvisorio, CronogramaEvento, DistribuicaoBolsa, AplicacaoEdital, NIVEL_BOLSA_CONFIG |
| `views.py` | Views de CRUD, PDF e candidaturas |
| `forms.py` | Formulários e formsets inline |
| `urls.py` | Rotas da app |
| `admin.py` | Admin com inlines |
| `templatetags/br_filters.py` | Filtro de formatação monetária |
