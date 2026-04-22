from django.core.management.base import BaseCommand

from users.models import Role, User


class Command(BaseCommand):
    help = "Create deterministic demo users for each role."

    def handle(self, *args, **options):
        default_password = "DemoPassword123!"
        demo_users = (
            ("admin@example.com", "admin", "Админ"),
            ("manager@example.com", "manager", "Менеджер"),
            ("user@example.com", "user", "Пользователь"),
            ("guest@example.com", "guest", "Гость"),
        )
        for email, role_code, first_name in demo_users:
            role = Role.objects.get(code=role_code)
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email.split("@", 1)[0],
                    "first_name": first_name,
                    "last_name": "Demo",
                    "patronymic": "Demo",
                    "role": role,
                    "is_active": True,
                },
            )
            if created:
                user.set_password(default_password)
                user.save(update_fields=["password"])
                self.stdout.write(self.style.SUCCESS(f"Created {email}"))
            else:
                if user.role_id != role_code:
                    user.role = role
                    user.save(update_fields=["role"])
                self.stdout.write(f"Already exists: {email}")

        self.stdout.write(
            self.style.WARNING(
                "Demo password for all users: DemoPassword123!"
            )
        )
