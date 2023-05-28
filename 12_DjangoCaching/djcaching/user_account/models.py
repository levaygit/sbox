from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name=_('user'))
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name=_('balance'))

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')