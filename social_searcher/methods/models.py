from django.db import models
from django.contrib.postgres.fields import JSONField
from django.conf import settings


class MethodResult(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    result = JSONField(blank=True, null=False)
    task_id = models.fields.CharField(max_length=100)
