from django.db import models


class TodoItem(models.Model):
    title = models.CharField(verbose_name='Task name', max_length=255)
    description = models.TextField(verbose_name='Task description')

    class Meta:
        verbose_name = 'Todo item'
        verbose_name_plural = 'Todo items'
        ordering = ['-id', ]

    def __str__(self):
        return self.title