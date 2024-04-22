from django.db import models
from users.models import CustomUser


# Create your models here.

class Color(models.Model):
    name = models.CharField(max_length=100)
    red = models.IntegerField(default=0)
    green = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)
    hue = models.FloatField(default=0)
    saturation = models.FloatField(default=0)
    lightness = models.FloatField(default=0)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_colors')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Palette(models.Model):
    name = models.CharField(max_length=100)
    colors = models.ManyToManyField(Color, related_name='palettes')
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_palettes')
    users_with_access = models.ManyToManyField(CustomUser, related_name='shared_palettes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + ' - ' + str(self.creator)
