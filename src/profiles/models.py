from django.db import models

# Create your models here.
class Subscription(models.Model):
    name = models.CharField(max_length=120)

    class Meta:
        permissions = [
            ("advanced", "Advanced Perm"),
            ("pro", "Pro Perm"),
            ("basic", "Basic Perm"),
            ("basic_ai", "Basic AI Perm"),

        ]
