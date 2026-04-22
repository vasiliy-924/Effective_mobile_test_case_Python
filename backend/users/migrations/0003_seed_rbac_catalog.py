from django.db import migrations


def seed_rbac_catalog(apps, schema_editor):
    Role = apps.get_model("users", "Role")
    BusinessElement = apps.get_model("users", "BusinessElement")
    AccessRoleRule = apps.get_model("users", "AccessRoleRule")

    roles = {
        "admin": "Администратор",
        "manager": "Менеджер",
        "user": "Пользователь",
        "guest": "Гость",
    }
    for code, name in roles.items():
        Role.objects.update_or_create(
            code=code,
            defaults={"name": name},
        )

    elements = {
        "book": "Книги",
        "order": "Заказы",
        "users": "Пользователи",
        "rules": "Правила доступа",
    }
    for code, name in elements.items():
        BusinessElement.objects.update_or_create(
            code=code,
            defaults={"name": name},
        )

    def upsert(role_code, element_code, **perms):
        element = BusinessElement.objects.get(code=element_code)
        AccessRoleRule.objects.update_or_create(
            role_id=role_code,
            element=element,
            defaults=perms,
        )

    # Admin can do everything with all managed elements.
    for element_code in ("book", "order", "users", "rules"):
        upsert(
            "admin",
            element_code,
            read_permission=True,
            read_all_permission=True,
            create_permission=True,
            update_permission=True,
            update_all_permission=True,
            delete_permission=True,
            delete_all_permission=True,
        )

    # Manager can read all books and orders, update own orders.
    upsert(
        "manager",
        "book",
        read_permission=True,
        read_all_permission=True,
        create_permission=False,
        update_permission=False,
        update_all_permission=False,
        delete_permission=False,
        delete_all_permission=False,
    )
    upsert(
        "manager",
        "order",
        read_permission=True,
        read_all_permission=True,
        create_permission=True,
        update_permission=True,
        update_all_permission=False,
        delete_permission=False,
        delete_all_permission=False,
    )

    # Regular user: can read books and work with own orders.
    upsert(
        "user",
        "book",
        read_permission=True,
        read_all_permission=True,
        create_permission=False,
        update_permission=False,
        update_all_permission=False,
        delete_permission=False,
        delete_all_permission=False,
    )
    upsert(
        "user",
        "order",
        read_permission=True,
        read_all_permission=False,
        create_permission=True,
        update_permission=True,
        update_all_permission=False,
        delete_permission=True,
        delete_all_permission=False,
    )

    # Guest: can read books list only.
    upsert(
        "guest",
        "book",
        read_permission=True,
        read_all_permission=True,
        create_permission=False,
        update_permission=False,
        update_all_permission=False,
        delete_permission=False,
        delete_all_permission=False,
    )
    upsert(
        "guest",
        "order",
        read_permission=False,
        read_all_permission=False,
        create_permission=False,
        update_permission=False,
        update_all_permission=False,
        delete_permission=False,
        delete_all_permission=False,
    )


def unseed_rbac_catalog(apps, schema_editor):
    AccessRoleRule = apps.get_model("users", "AccessRoleRule")
    BusinessElement = apps.get_model("users", "BusinessElement")

    AccessRoleRule.objects.filter(
        element__code__in=("book", "order", "users", "rules")
    ).delete()
    BusinessElement.objects.filter(
        code__in=("book", "order", "users", "rules")
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_seed_roles_and_access_rules"),
    ]

    operations = [
        migrations.RunPython(seed_rbac_catalog, unseed_rbac_catalog),
    ]
