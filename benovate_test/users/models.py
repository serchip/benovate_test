from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext_lazy as _

from shippets.models import MoneyField


class User(AbstractUser):
    INN = models.PositiveIntegerField(_('ИНН'), validators=[MaxValueValidator(999999999999)], null=True, blank=True)
    balance = MoneyField(verbose_name=_('Счет'), max_digits=8, decimal_places=2, default=0)
