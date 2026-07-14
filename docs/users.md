# Usuários do Sistema

> Os usuários abaixo são gerados pelo comando `python manage.py gerar_dados_fake`.
> A senha padrão de todos é: **`senha123`**

---

## Credenciais

| Email | Nome | Tipo / Grupo |
|---|---|---|
| `admin@email.com` | Administrador do Sistema | **Superuser** (acesso total) |
| `manager1@email.com` | Zoe Abreu | Manager |
| `manager2@email.com` | Ana Cecília da Rocha | Manager |
| `manager3@email.com` | Evelyn Farias | Manager |
| `executor1@email.com` | Maria Liz Montenegro | ExecuteUser |
| `executor2@email.com` | Juan Moura | ExecuteUser |
| `executor3@email.com` | Emanuella Marques | ExecuteUser |
| `bolsista1@email.com` | Dr. Diego da Luz | ViewUser |
| `bolsista2@email.com` | Luan Viana | ViewUser |
| `bolsista3@email.com` | José Pedro Araújo | ViewUser |
| `bolsista4@email.com` | Erick da Mota | ViewUser |
| `bolsista5@email.com` | Dr. Luigi da Rocha | ViewUser |
| `bolsista6@email.com` | André Souza | ViewUser |
| `bolsista7@email.com` | Elisa da Conceição | ViewUser |
| `bolsista8@email.com` | Oliver Cardoso | ViewUser |
| `bolsista9@email.com` | Théo Farias | ViewUser |
| `bolsista10@email.com` | Pedro Lucas Pereira | ViewUser |
| `bolsista11@email.com` | Samuel Teixeira | ViewUser |
| `bolsista12@email.com` | Luiz Gustavo Almeida | ViewUser |
| `bolsista13@email.com` | João Pedro da Mata | ViewUser |
| `bolsista14@email.com` | Allana Rocha | ViewUser |
| `bolsista15@email.com` | Pedro Henrique Ramos | ViewUser |

---

## Permissões por grupo

| Grupo | Permissões |
|---|---|
| **Superuser** | Acesso total: admin Django, gerenciar usuários, criar/editais, avaliar, aprovar |
| **Manager** | Criar e gerenciar editais, aprovar usuários, avaliar candidatos, visualizar painéis |
| **ExecuteUser** | Acesso operacional (execução de tarefas do sistema) |
| **ViewUser** | Visualizar editais abertos, candidatar-se, acompanhar status |

---

## Recuperação de senha

Caso esqueça a senha, acesse a tela de login e clique em **"Esqueci minha senha"**.  
Em ambiente de desenvolvimento, o link de redefinição aparece nos logs do container:

```powershell
docker compose logs web
```

Em produção, o email é enviado via SMTP.

---

## Comandos dos containers Docker

### Subir todos os containers (dev)

```powershell
# Na raiz do projeto (onde está o docker-compose.yml)
docker compose up -d
```

A aplicação ficará disponível em:
- **http://localhost** (via Traefik, porta 80)
- **http://localhost:8000** (direto no Django, porta 8000)
- RabbitMQ Management: http://localhost:15672 (guest/guest)

### Parar todos os containers

```powershell
docker compose down
```

### Parar sem perder dados (volumes preservados)

```powershell
docker compose stop
```

### Reiniciar um container específico

```powershell
# Ex: após editar .env ou código Python que não é auto-recarregado
docker compose restart web
docker compose restart celery
```

### Ver logs de um container

```powershell
docker compose logs web        # logs do Django
docker compose logs celery     # logs das tarefas assíncronas
docker compose logs db         # logs do PostgreSQL

# Seguir em tempo real
docker compose logs -f web
```

### Executar comandos Django dentro do container

```powershell
# Shell do Django
docker compose exec web python manage.py shell

# Aplicar migrations
docker compose exec web python manage.py migrate

# Gerar dados fake (popula o banco)
docker compose exec web python manage.py gerar_dados_fake

# Limpar e regenerar todos os dados
docker compose exec web python manage.py gerar_dados_fake --limpar

# System check
docker compose exec web python manage.py check
```

### Recriar containers (após mudanças no Dockerfile)

```powershell
docker compose up -d --build
```

### Apagar tudo (containers + volumes + dados)

```powershell
docker compose down -v
```

### Ver status dos containers

```powershell
docker compose ps
```

---

## Serviços

| Container | Descrição | Porta |
|---|---|---|
| `db` | PostgreSQL 16 | (interna) |
| `redis` | Cache e backend Celery | (interna) |
| `rabbitmq` | Message broker Celery | 15672 (management) |
| `web` | Django runserver | 8000 |
| `celery` | Worker de tarefas assíncronas | (interna) |
| `celery-beat` | Agendador de tarefas periódicas | (interna) |
| `traefik` | Proxy reverso | 80 (app), 8080 (dashboard) |
