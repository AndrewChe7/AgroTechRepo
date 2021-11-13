from django.db import models
from django.contrib.auth.models import User


class UserTypes(models.IntegerChoices):
    RETAIL_PURCHASER = 0, 'Розничный закупщик'
    WHOLESALE_PURCHASER = 1, 'Оптовый закупщик'
    PROVIDER = 2, 'Поставщик'
    TRANSFER = 3, 'Перевозчик'


class UserInfo (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_info')
    user_type = models.IntegerField(default=UserTypes.RETAIL_PURCHASER, choices=UserTypes.choices)

    def __str__(self):
        return str(self.user)
