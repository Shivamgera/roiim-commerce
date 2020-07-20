from django.db import models
from django.conf import settings


class AuditModel(models.Model):
    """
    Abstract Audit model class to be used in all the models
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(AuditModel):
    """
    Model to store Product Details
    """
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,)
    is_visible = models.BooleanField(default=True)

    class Meta:
        app_label = "product"
        ordering = ("name",)

    @staticmethod
    def get_all_products():
        return Product.objects.all()