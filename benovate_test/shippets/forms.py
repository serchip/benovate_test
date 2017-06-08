from django.forms import DecimalField


#------------Money---------------------------------
class MoneyFormField(DecimalField):
    """Денежное поле"""
    def __init__(self, **kwargs):
        kwargs['min_value'] = kwargs.get('min_value', None) and kwargs['min_value'] or 0
        kwargs['max_digits'] = kwargs.get('max_digits', None) and kwargs['max_digits'] or 13
        kwargs['decimal_places'] = kwargs.get('decimal_places', None) and kwargs['decimal_places'] or 2
        super(MoneyFormField, self).__init__(**kwargs)

    def to_python(self, value):
        if value:
            value = value.replace("руб", "").replace("Р", "")
        return super(MoneyFormField, self).to_python(value)
