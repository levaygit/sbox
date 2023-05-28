from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        ordering = ["name", "price"]

    name = models.CharField(max_length=100, verbose_name=_('name'))
    description = models.TextField(null=False, blank=True, verbose_name=_('description'))
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_('price'))
    discount = models.SmallIntegerField(default=0, verbose_name=_('discount'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    archived = models.BooleanField(default=False, verbose_name=_('archived'))

    def __str__(self):
        return _("Product(pk={}, name={})").format(self.pk, self.name)


class Order(models.Model):
    delivery_address = models.TextField(null=True, blank=True, verbose_name=_('delivery address'))
    promocode = models.CharField(max_length=20, null=False, blank=True, verbose_name=_('promocode'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=_('user'))
    products = models.ManyToManyField(Product, related_name="orders", verbose_name=_('products'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')


class Shop(models.Model):
    name = models.CharField(max_length=20, null=False, blank=True, verbose_name=_('name'))
    address = models.CharField(max_length=100, null=False, blank=True, verbose_name=_('address'))
    opening = models.TimeField(verbose_name=_('opening'))
    closing = models.TimeField(verbose_name=_('closing'))

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')


class Promotion(models.Model):
    name = models.CharField(max_length=20, null=False, blank=True, verbose_name=_('name'))
    description = models.TextField(null=False, blank=True, verbose_name=_('description'))
    start = models.DateField(verbose_name=_('start'))
    end = models.DateField(verbose_name=_('end'))
    users = models.ManyToManyField(
        User,
        related_name="users",
        default=None,
        null=True,
        verbose_name=_('users'),
    )
    products = models.ManyToManyField(
        Product,
        related_name="products",
        default=None,
        null=True,
        verbose_name=_('products'),
    )

    class Meta:
        verbose_name = _('promotion')
        verbose_name_plural = _('promotions')
