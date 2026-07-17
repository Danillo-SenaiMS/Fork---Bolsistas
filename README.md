# Bolsas SENAI-MS

Sistema de gestao de bolsas de estudo para os institutos SENAI de Mato Grosso do Sul. Plataforma completa para criacao de editais, cadastro de candidatos, avaliacao e acompanhamento de bolsistas.

## Funcionalidades

- **Editais** — Criacao, edicao e publicacao de editais com modalidades (nivel 1 a 4), requisitos de qualificacao e experiencia, valores escalonados e cronograma de etapas
- **Candidaturas** — Cadastro completo de bolsistas (dados pessoais, formacao, documentos), inscricao em editais e acompanhamento de status
- **Classificacao** — Criterios de pontuacao customizaveis (publicacoes, eventos, cursos) e avaliacao individual de candidatos
- **IA** — Analise de editais e compatibilidade de candidatos via IA (Groq / Llama 3.3), com suporte a processamento assincrono (Celery)
- **Painel** — Dashboard para bolsistas ativos com acompanhamento de etapas
- **Permissoes** — Controle de acesso por grupos (Manager, ExecuteUser, ViewUser, SuperUser)
- **PDF** — Geracao de editais em PDF
- **Notificacoes** — Sistema de notificacoes para usuarios

## Stack

| Camada | Tecnologia |
|---|---|
| Web | Django 6.0 + HTMX + Bootstrap 5 |
| Tarefas | Celery + RabbitMQ |
| Cache | Redis |
| DB | PostgreSQL 16 |
| IA | Groq API (Llama 3.3 70B, OpenAI-compatible) |
| Infra | Docker + Docker Compose (dev) / Docker Swarm (prod) |
| Proxy | Traefik v3 (Let's Encrypt automatico em producao) |

## Pre-requisitos

- Python 3.12+
- Docker e Docker Compose (opcional, para desenvolvimento containerizado)
- PostgreSQL (ja incluso no docker-compose)
- RabbitMQ e Redis (ja inclusos no docker-compose)

## Setup Local (sem Docker)

```bash
# Clone o repositorio
git clone <repo-url>
cd Fork---Bolsistas

# Crie e ative ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows

# Instale dependencias
pip install -r requirements.txt

# Configure variaveis de ambiente
cp .env.example .env
# Edite .env com suas credenciais (SECRET_KEY, DB_*, etc.)

# Execute migracoes
python manage.py migrate

# Crie superusuario
python manage.py createsuperuser

# Inicie o servidor
python manage.py runserver
```

## Setup com Docker (recomendado)

```bash
# Clone o repositorio
git clone <repo-url>
cd Fork---Bolsistas

# Copie e configure .env
cp .env.example .env

# Inicie os servicos
docker compose up -d

# Execute migracoes
docker compose exec web python manage.py migrate

# Crie superusuario
docker compose exec web python manage.py createsuperuser

# Acesse http://bolsas.localhost
```

### Servicos Docker

| Servico | Porta | Descricao |
|---|---|---|
| web | 8000 | Django (runserver em dev / gunicorn em prod) |
| celery | — | Worker para tarefas assincronas (IA) |
| celery-beat | — | Agendador de tarefas periodicas |
| db | 5432 | PostgreSQL |
| redis | 6379 | Cache e backend de resultados Celery |
| rabbitmq | 5672 / 15672 | Broker de mensagens Celery |
| traefik | 80 / 8080 | Proxy reverso (dashboard em :8080) |

## Variaveis de Ambiente

| Variavel | Obrigatoria | Padrao | Descricao |
|---|---|---|---|
| `SECRET_KEY` | Sim | — | Chave secreta Django |
| `DEBUG` | Nao | `False` | Modo debug |
| `ALLOWED_HOSTS` | Nao | `localhost,127.0.0.1` | Hosts permitidos |
| `DB_ENGINE` | Nao | `sqlite3` | Engine do banco |
| `DB_NAME` | Nao | `db.sqlite3` | Nome do banco |
| `DB_HOST` | Nao | — | Host do PostgreSQL |
| `DB_USER` | Nao | — | Usuario do PostgreSQL |
| `DB_PASSWORD` | Nao | — | Senha do PostgreSQL |
| `CELERY_BROKER_URL` | Nao | `amqp://guest:guest@rabbitmq:5672//` | URL do broker |
| `CACHE_URL` | Nao | `redis://redis:6379/1` | URL do cache Redis |
| `GROQ_API_KEY` | Nao | — | Chave da API Groq para IA |
| `IA_ASYNC` | Nao | `False` | Processar IA de forma assincrona |
| `EMAIL_HOST` | Nao | `smtp.gmail.com` | Servidor SMTP |

## Grupos de Usuario

| Grupo | Permissoes |
|---|---|
| **SuperUser** | Acesso total: criar/editar/aprovar editais, alterar status, ver informacoes administrativas e IA |
| **Manager** | Criar/editar editais, ver candidatos, aprovar editais (validar). Nao ve Informacoes administrativas |
| **ExecuteUser** | Criar/editar editais, ver candidatos e informacoes administrativas. Nao aprova editais |
| **ViewUser** | Visualizar editais, candidatar-se, ver propria compatibilidade via IA |

## Estrutura do Projeto

```
.
├── accounts/          # Model User customizado (email-based auth)
├── base/              # Mixins, middleware, context processors, utilitarios
├── cadastro/          # Cadastro de bolsistas (dados pessoais, formacao)
├── classificacao/     # Criterios de pontuacao e avaliacao
├── config/            # Settings Django (settings.py, urls.py, wsgi.py)
├── docker/            # Entrypoints Docker (web + celery)
├── editais/           # Editais (modelos, formularios, views, migrations)
├── notifications/     # Sistema de notificacoes
├── painel_bolsistas/  # Dashboard de bolsistas
├── static/            # Arquivos estaticos
├── templates/         # Templates Django
├── docker-compose.yml       # Ambiente de desenvolvimento
├── docker-compose.prod.yml  # Ambiente de producao (Docker Swarm)
├── Dockerfile               # Imagem Docker
├── requirements.txt         # Dependencias Python
└── manage.py                # CLI Django
```

## Comandos Uteis

```bash
# Migracoes
docker compose exec web python manage.py makemigrations
docker compose exec web python manage.py migrate

# Celery
docker compose exec celery celery -A config worker -l info

# Logs
docker compose logs -f web

# Shell Django
docker compose exec web python manage.py shell

# Testes
docker compose exec web python manage.py test
```
