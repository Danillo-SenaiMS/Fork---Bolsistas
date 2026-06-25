# Notifications

App responsável pelo sistema de notificações in-app, disparadas automaticamente por sinais (signals) do Django.

## Modelos

### `Notificacao`
Notificação para um usuário:
- `destinatario` — FK para User
- `titulo` — Título da notificação
- `mensagem` — Corpo da mensagem
- `lido` — Flag de leitura (bool, default False)
- `tipo` — Categoria: cadastro, classificacao, solicitacao, sistema

## Signals

Os sinais são registrados em `notifications/apps.py:ready()` e criam notificações automaticamente:

### `notificar_cadastro`
Disparado no `post_save` de `CadastroBolsista`. Quando um novo cadastro é criado, notifica o bolsista.

### `notificar_classificacao`
Disparado no `post_save` de `Classificacao`. Quando uma classificação com pontuação > 0 é salva, notifica o bolsista com o nome do edital e a pontuação total.

### `notificar_solicitacao`
Disparado no `post_save` de `SolicitacaoEdicao`:
- **Status pendente**: Notifica todos os gestores (ADMIN/MANAGER)
- **Status aprovado**: Notifica o bolsista que a solicitação foi aprovada
- **Status rejeitado**: Notifica o bolsista que a solicitação foi rejeitada

## Views

### `NotificacaoListView`
Listagem de notificações do usuário.

### `MarcarLidaView`
Marca uma notificação específica como lida.

### `MarcarTodasLidasView`
Marca todas as notificações do usuário como lidas.

## URLs

| Path | View | Nome |
|------|------|------|
| (vazio) | NotificacaoListView | `notificacao_list` |
| `<pk>/marcar-lida/` | MarcarLidaView | `marcar_lida` |
| `marcar-todas-lidas/` | MarcarTodasLidasView | `marcar_todas_lidas` |

## Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `models.py` | Notificacao |
| `views.py` | Views de listagem e marcação de leitura |
| `signals.py` | Sinais automáticos de notificação |
| `apps.py` | Config com `ready()` para registro de sinais |
| `urls.py` | Rotas da app |
