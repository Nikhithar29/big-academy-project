from django.db import models
from django.conf import settings


class Module(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ModuleStep(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('VIDEO', 'Video'),
        ('PDF', 'PDF'),
        ('TEXT', 'Text'),
    ]

    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='steps')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    content_url = models.URLField()
    order_number = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.module.title} - {self.title}"
