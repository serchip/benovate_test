from django.db import models

from shippets.forms import MoneyFormField


#===============================================================================
# In all fields, where money are stored, we should use this class!!!
#===============================================================================
class MoneyField(models.DecimalField):
    """Денежное поле"""
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        super(MoneyField, self).__init__(verbose_name, name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'max_digits': self.max_digits,
            'decimal_places': self.decimal_places,
            'min_value': self.min_value,
            'max_value': self.max_value,
            'form_class': MoneyFormField,
        }
        defaults.update(kwargs)
        return super(MoneyField, self).formfield(**defaults)
