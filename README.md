# Effective Mobile Test Case (Django)

Backend API с разделением аутентификации и авторизации:
- аутентификация через JWT;
- авторизация через собственную RBAC-модель (`Role`, `BusinessElement`, `AccessRoleRule`);
- защищенные mock-ресурсы с корректной семантикой `401/403`;
- API управления правилами доступа только для роли `admin`.

## Архитектура

1. **Authentication (кто пользователь)**  
   JWT access/refresh токены, login/logout/register, soft-delete через `is_active=False`.
2. **Authorization (что пользователь может делать)**  
   Проверка доступа по таблице правил `AccessRoleRule`.
3. **Business mocks**  
   Простые endpoint'ы `/api/demo/*`, которые демонстрируют применение правил доступа.

Подробности по таблицам и правилам в [db.md](db.md).

## Технологии

- Python 3.12+
- Django 6
- Django REST Framework
- djangorestframework-simplejwt
- PostgreSQL (по env) или SQLite (fallback для локального запуска)
- pytest + pytest-django

## Быстрый старт

### 1) Локально без Docker

```bash
cd backend
python3 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py seed_demo_users
python3 manage.py runserver
```

### 2) С Docker Compose

```bash
docker compose -f docker-compose.yml up --build
```

## Переменные окружения

Скопируйте `.env.example` в `.env` и заполните значения.

Ключевые переменные:
- `SECRET_KEY`
- `DJANGO_DEBUG`
- `ALLOWED_HOSTS`
- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `DB_HOST`
- `DB_PORT`

## API Контракт

### Auth
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `POST /api/auth/token/refresh/`

### Current user
- `GET /api/users/me/`
- `PATCH /api/users/me/`
- `POST /api/users/me/delete/` (soft-delete + optional refresh blacklist)

### RBAC rules (admin only)
- `GET /api/rules/`
- `POST /api/rules/`
- `GET /api/rules/{id}/`
- `PATCH /api/rules/{id}/`
- `DELETE /api/rules/{id}/`

### Demo resources
- `GET /api/demo/books/`
- `GET /api/demo/order/{id}/`

## Логика 401/403

- `401 Unauthorized` — пользователь не аутентифицирован (нет/невалидный JWT).
- `403 Forbidden` — пользователь аутентифицирован, но правило в `AccessRoleRule` не разрешает действие.

## Тестовые данные

После миграций:
```bash
python manage.py seed_demo_users
```

Демо-пользователи создаются с паролем `DemoPassword123!`:
- `admin@example.com`
- `manager@example.com`
- `user@example.com`
- `guest@example.com`

## Тесты

```bash
cd backend
pytest
```

## Автор
### **Василий Петров** 
    - [GitHub github.com/vasiliy-924](https://github.com/vasiliy-924)
    - [TG t.me/thunderbasil](https://t.me/thunderbasil)