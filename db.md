# DB Design: Authentication and Authorization

## 1) Authentication model

`users.User` (кастомная модель пользователя):
- `first_name`
- `last_name`
- `patronymic`
- `email` (login field)
- `username` (технический уникальный идентификатор)
- `password` (хэш через Django hashers)
- `is_active` (soft-delete флаг)
- `role` -> FK на `Role.code`
- `avatar`

### Почему так
- `email` как логин — привычный UX.
- `is_active=False` поддерживает мягкое удаление без потери данных.
- Хранение пароля делегировано стандартной системе Django, без кастомной криптографии.

## 2) Authorization model (RBAC)

### `Role`
Справочник ролей:
- `admin`
- `manager`
- `user`
- `guest`

### `BusinessElement`
Справочник бизнес-элементов API:
- `book`
- `order`
- `users`
- `rules`

### `AccessRoleRule`
Правило доступа для пары `(role, element)`:
- `read_permission`
- `read_all_permission`
- `create_permission`
- `update_permission`
- `update_all_permission`
- `delete_permission`
- `delete_all_permission`

Есть ограничение уникальности: одна запись правил на одну пару `role + element`.

## 3) Семантика полей `*_permission`

- `*_all_permission=True` — действие разрешено над любым объектом элемента.
- `*_permission=True` и `*_all_permission=False` — действие разрешено только над “своими” объектами (`owner_id == request.user.id`).
- оба `False` — действие запрещено.

### Пример чтения
- `read_all_permission=True` -> можно читать все объекты.
- `read_permission=True` -> можно читать только собственные.

## 4) Разделение authn vs authz

- **Authentication** отвечает на вопрос: “кто делает запрос?”  
  Реализовано через JWT (`Bearer access_token`) и `request.user`.
- **Authorization** отвечает на вопрос: “что разрешено этому пользователю?”  
  Реализовано через lookup в `AccessRoleRule`.

Это разделение делает систему прозрачной:
- проще тестировать;
- проще расширять правила без переписывания endpoint'ов;
- проще объяснить ревьюеру.