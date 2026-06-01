# TaskFlow API

TaskFlow API - backend-сервис для управления задачами, построенный на FastAPI с использованием PostgreSQL, Redis и RabbitMQ.

## Возможности

- Регистрация пользователей
- JWT-аутентификация
- Авторизация через Bearer Token
- CRUD для задач
- Кэширование через Redis
- Асинхронная обработка событий через RabbitMQ
- Dead Letter Queue (DLQ)
- Миграции Alembic
- Docker Compose окружение
- Автоматические тесты

---

## Технологии

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy Async
- Alembic
- Redis
- RabbitMQ
- aio-pika
- JWT
- Pytest
- Docker
- Docker Compose

---

## Архитектура

```text
Client
   │
   ▼
FastAPI
   │
   ├── PostgreSQL
   │
   ├── Redis Cache
   │
   └── RabbitMQ
          │
          ▼
       Worker
```

---

## Запуск проекта

### Клонирование

```bash
git clone https://github.com/your_username/taskflow-api.git

cd taskflow-api
```

### Настройка окружения

```bash
cp .env.example .env
```

### Запуск контейнеров

```bash
docker compose up -d
```

### Применение миграций

```bash
docker compose exec app alembic upgrade head
```

---

## Swagger

После запуска:

```text
http://localhost:8000/docs
```

---

## API

### Auth

#### Регистрация

```http
POST /auth/register
```

```json
{
  "email": "user@example.com",
  "password": "123456"
}
```

#### Логин

```http
POST /auth/login
```

```json
{
  "email": "user@example.com",
  "password": "123456"
}
```

---

### Tasks

#### Создать задачу

```http
POST /tasks
```

#### Получить список задач

```http
GET /tasks
```

#### Обновить задачу

```http
PATCH /tasks/{id}
```

#### Удалить задачу

```http
DELETE /tasks/{id}
```

---

## RabbitMQ Events

При регистрации пользователя публикуется событие:

```json
{
  "event": "user_registered",
  "email": "user@example.com"
}
```

Worker получает событие и обрабатывает его асинхронно.

Поддерживается Dead Letter Queue для сообщений с ошибками.

---

## Тестирование

Запуск тестов:

```bash
docker compose exec app pytest -v
```

Текущее состояние:

```text
8 passed
```

Тестируются:

- регистрация пользователя
- логин пользователя
- получение текущего пользователя
- health endpoint
- создание задачи
- получение задач
- обновление задачи
- удаление задачи

---
