from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title