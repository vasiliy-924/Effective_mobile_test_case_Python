# Effective_mobile_test_case_Python
Тестовое задание от компании Effective mobile. Язык Python.

## Основные возможности

- Аутентификация по токену: выдача/удаление токена
    - POST /api/auth/token/login
    - POST /api/auth/token/logout
- Пользователи и профиль: список, профиль, "Я", аватар, подписки
    - GET /api/users
    - GET /api/users/{id}/
    - GET /api/users/me/
    - PUT /api/users/me/avatar
    - 

Полная спецификация в OpenAPI - в docs.openapi-schema.yml

## Стэк
Backend: Python 3.12, Django, Django REST Framework, ((Djoser, django-filter, Gunicorn, PostgreSQL))
Infra: Docker, Docker Compose

## Запуск локально (Docker Compose)
```bash
docker compose -f docker-compose-yml up --build
```

## Конфигурация окружения 
.env.example


## Наполнение тестовыми данными


## Автор
### **Василий Петров** 
    - [GitHub github.com/vasiliy-924](https://github.com/vasiliy-924)
    - [TG t.me/thunderbasil](https://t.me/thunderbasil)