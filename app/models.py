from django.db import models
from django.contrib.auth.models import User


class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(verbose_name='Task name', max_length=255)
    description = models.TextField(verbose_name='Task description')

    class Meta:
        verbose_name = 'Todo item'
        verbose_name_plural = 'Todo items'


    def __str__(self):
        return self.title