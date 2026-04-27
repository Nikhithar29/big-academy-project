from django.db import models
from django.conf import settings
from modules_app.models import Module


class Certificate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=100, unique=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'module'], name='unique_user_module_certificate')
        ]

    def __str__(self):
        return f"{self.user.email} - {self.module.title}"