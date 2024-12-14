from django.db import models
from django.conf import settings
from django.utils.timezone import now


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SearchHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.email} - {self.query}"

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_entries'  # related_name を修正
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        related_name='favorited_by_users'  # related_name を修正
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
