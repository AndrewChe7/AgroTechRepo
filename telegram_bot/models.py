from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.

class TelegramInfo(models.Model):
    user = models.OneToOneField(auth_models.User, on_delete=models.CASCADE, related_name="telegram_info")
    chat_id = models.BigIntegerField(default=None, null=True, blank=True)
    