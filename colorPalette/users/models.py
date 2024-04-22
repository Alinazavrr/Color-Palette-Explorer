from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    icon = models.ImageField(upload_to='user_icons', null=True, blank=True)
