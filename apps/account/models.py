import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        unique=True,
    )
    username = models.CharField(
        max_length=100,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]


class Profile(models.Model):
    """Модель профиля пользователя для дополнительной личной информации"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return f"Profile(user={self.user})"
