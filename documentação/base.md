# Base

App fundamental do projeto que fornece a infraestrutura compartilhada por todas as outras apps.

## Modelos

### `DataModel`
Modelo abstrato base com campos de auditoria:
- `created_at` — Data/hora de criação (auto)
- `updated_at` — Data/hora de última atualização (auto)

Todos os modelos das demais apps herdam deste modelo.

## Managers

### `TenantManager`
Manager customizado que filtra automaticamente os objetos pelo tenant atual (armazenado em thread-local via `base/tenant.py`). Garante isolamento multi-tenant em todas as consultas.

## Middleware

### `TenantMiddleware`
Extrai o tenant do subdomínio da requisição e o armazena em thread-local storage. Executado após `AuthenticationMiddleware`.

### `LoginRequiredMiddleware`
Redireciona usuários não autenticados para a página de login. Possui uma lista de paths públicos permitidos: `/`, `/login/`, `/registro/`, `/admin/`, `/static/`, `/media/`.

## Mixins

### `TenantRequiredMixin`
Valida que o usuário autenticado possui um tenant associado. Usado em views que exigem contexto multi-tenant.

### `RoleRequiredMixin`
Restringe acesso baseado no tipo de perfil (`tipo`) do usuário.

### `ManagerRequiredMixin`
Restringe acesso a usuários com perfil `ADMIN` ou `MANAGER`.

### `AdminRequiredMixin`
Restringe acesso apenas a usuários com perfil `ADMIN`.

## Views

### `media_protegida`
View que serve arquivos de mídia com controle de acesso, validando se o usuário tem permissão para acessar o arquivo solicitado. Bloqueia path traversal.

## Comandos de Gestão

### `seed_data`
Popula o banco de dados com dados de demonstração: tenants (SESI, SENAI), usuários por tenant, cadastros de bolsistas, editais, aplicações e classificações. Utiliza a biblioteca Faker com locale pt_BR.

## Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `models.py` | `DataModel` (base abstrata) |
| `managers.py` | `TenantManager` |
| `tenant.py` | Thread-local tenant storage |
| `tenant_middleware.py` | `TenantMiddleware` |
| `middleware.py` | `LoginRequiredMiddleware` |
| `mixins.py` | Mixins de controle de acesso |
| `views.py` | `media_protegida` |
| `management/commands/seed_data.py` | Comando de seed do banco |
