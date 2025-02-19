from django.db import models

# Create your models here.


class Library(models.Model):
    status = models.BooleanField(default=True)
    name = models.CharField(max_length=255, default=None, null=True)

    def __str__(self) -> str:
        return self.name