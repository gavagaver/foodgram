from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = (
            'id',
        )

    def __str__(self):
        return f'{self.username} ({self.first_name} {self.last_name})'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Подписчик",
        related_name='subscribers',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        related_name='subscribe',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = (
            '-id',
        )
        constraints = (
            models.UniqueConstraint(
                fields=(
                    'user',
                    'author',
                ),
                name='unique_subscription'
            ),
        )
