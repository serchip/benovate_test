from django.contrib.auth import get_user_model
from django import forms


class BalanceForm(forms.Form):
    user_from = forms.ModelChoiceField(queryset=get_user_model().objects.filter(is_active=True), required=True,
                                       help_text="User from"
                                       )
    users_to = forms.ModelMultipleChoiceField(queryset=get_user_model().objects.filter(is_active=True), required=True,
                                              help_text="List Users to"
                                              )
    dec_sum = forms.DecimalField(required=True, min_value=0, max_digits=8, decimal_places=2)
