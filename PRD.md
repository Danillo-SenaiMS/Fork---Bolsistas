# 📌 PLANO DE DESENVOLVIMENTO EM SPRINTS — PORTAL DA INOVAÇÃO (DJANGO SaaS)

## 🎯 VISÃO GERAL

Projeto estruturado em sprints curtas com foco em:

* Entregas incrementais
* Validação contínua
* Base sólida de arquitetura SaaS multi-tenant

---

# 🟦 SPRINT 0 — SETUP E FUNDAÇÃO DO PROJETO

## Objetivo

Estabelecer base técnica e estrutural do projeto.

## Atividades

### Ambiente

* Criar repositório do projeto
* Configurar ambiente virtual Python
* Instalar Django + dependências iniciais
* Criar arquivo `requirements.txt`

### Estrutura inicial

* Criar projeto Django (`config`)
* Criar apps base:

  * base
  * accounts
* Organizar estrutura de pastas (apps na raiz)

### Configurações

* Configurar `.env` com:

  * SECRET_KEY
  * DB
  * EMAIL
* Integrar `python-decouple` no `settings.py`
* Configurar PostgreSQL

### Padrões globais

* Ajustar:

  * timezone: America/Campo_Grande
  * idioma: pt-BR
* Criar model base com:

  * created_at
  * updated_at

---

# 🟦 SPRINT 1 — AUTENTICAÇÃO E USUÁRIOS

## Objetivo

Implementar sistema de autenticação com roles.

## Atividades

### Modelagem

* Criar User customizado:

  * login via email
  * remover username
* Criar campos:

  * nome completo
  * telefone
  * tipo usuário

### Roles

* Implementar:

  * ADMIN
  * MANAGER
  * COMMON
* Criar lógica de permissões

### Views e fluxo

* Tela de:

  * login
  * cadastro
* Validações:

  * externo → upload obrigatório
  * colaborador → unidade obrigatória

### Segurança

* Proteção de rotas com login obrigatório
* Redirecionamento pós-login

---

# 🟦 SPRINT 2 — MULTI-TENANT (CORE CRÍTICO)

## Objetivo

Implementar isolamento de dados entre tenants.

## Atividades

### Modelagem

* Adicionar `tenant_id` em models base

### Middleware

* Criar middleware de tenant:

  * identificar tenant por usuário/logado
  * injetar no request

### Query Filtering

* Implementar filtro automático por tenant

### Segurança de arquivos

* Proteger media files por tenant
* Garantir acesso restrito

---

# 🟦 SPRINT 3 — CADASTRO DE BOLSISTAS

## Objetivo

Construir módulo completo de cadastro.

## Atividades

### Models

* Criar entidade Bolsista:

  * dados pessoais
  * acadêmicos
  * documentos

### Regras

* Validar idade (>18 anos)
* Suporte a múltiplos cursos

### Uploads

* Implementar:

  * currículo
  * documentos
  * foto

### Views

* Criar CRUD com CBVs

---

# 🟦 SPRINT 4 — EDITAIS

## Objetivo

Criar sistema de gestão de editais.

## Atividades

### Models

* Criar entidade Edital:

  * nome
  * descrição
  * requisitos
  * status

### Permissões

* Manager:

  * cria/edita
* Common:

  * apenas visualiza

### Views

* Listagem de editais
* Detalhamento

---

# 🟦 SPRINT 5 — APLICAÇÕES EM EDITAIS

## Objetivo

Permitir candidatura e acompanhamento.

## Atividades

### Models

* Criar entidade Aplicação:

  * usuário
  * edital
  * status

### Fluxo

* Aplicar em edital
* Evitar duplicidade

### Views

* Tela de:

  * inscrição
  * acompanhamento

---

# 🟦 SPRINT 6 — CLASSIFICAÇÃO

## Objetivo

Sistema de pontuação de bolsistas.

## Atividades

### Models

* Criar entidade Classificação:

  * pontuação
  * critérios (flexível)

### Permissões

* Apenas MANAGER pode classificar

### Lógica

* Vincular classificação à aplicação

### Notificação

* Disparo de e-mail automático

---

# 🟦 SPRINT 7 — NOTIFICAÇÕES (CELERY)

## Objetivo

Implementar processamento assíncrono.

## Atividades

### Setup

* Configurar:

  * Redis
  * Celery

### Funcionalidades

* Envio de e-mails:

  * classificação
  * cadastro

---

# 🟦 SPRINT 8 — DASHBOARD

## Objetivo

Criar visão gerencial.

## Atividades

### Funcionalidades

* Resumo de:

  * usuários
  * aplicações
  * classificações

### UI

* Kanban ou cards simples

---

# 🟦 SPRINT 9 — UI/UX E FRONTEND

## Objetivo

Refinar experiência do usuário.

## Atividades

### Layout

* Criar base.html
* Navbar padrão

### Estilo

* Aplicar:

  * Bootstrap 5
  * cores azul/branco

### Interatividade

* Implementar HTMX:

  * formulários dinâmicos
  * atualizações parciais

---

# 🟦 SPRINT 10 — SEED DE DADOS

## Objetivo

Gerar dados para demonstração.

## Atividades

### Django Command

* Criar comando customizado:

  * usuários variados
  * editais
  * aplicações
  * classificações

### Cenários

* Simular:

  * múltiplos tenants
  * diferentes datas

---

# 🟦 SPRINT 11 — HARDENING E FINALIZAÇÃO

## Objetivo

Preparar sistema para produção.

## Atividades

### Segurança

* Revisar permissões
* Validar acesso a arquivos

### Configuração

* Ajustar:

  * S3
  * variáveis de ambiente

### Performance

* Revisar queries
* Otimizar carregamentos

---

# 📊 ORDEM DE PRIORIDADE CRÍTICA

1. Autenticação
2. Multi-tenant
3. Cadastro
4. Editais
5. Aplicações
6. Classificação
7. Notificações

---

# ⚠️ RISCOS PRINCIPAIS

* Erro no isolamento multi-tenant
* Complexidade desnecessária na modelagem
* Falhas de permissão
* Uploads inseguros

---

# ✅ DEFINIÇÃO DE PRONTO (DoD)

Cada sprint deve:

* Código funcional
* Sem erros críticos
* Seguindo padrões definidos
* Integrado ao fluxo do sistema

---
