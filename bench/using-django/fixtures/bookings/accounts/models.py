from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        MEMBER = "member", "Member"
        SUPPORT = "support", "Support"
        MANAGER = "manager", "Manager"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    def save(self, *args, **kwargs):
        # Staff access follows the role.
        self.is_staff = self.role in (self.Role.SUPPORT, self.Role.MANAGER)
        super().save(*args, **kwargs)
