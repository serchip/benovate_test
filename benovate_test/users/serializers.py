from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.db.models import F
from django.db import transaction
from rest_framework import exceptions, serializers

from .models import User

UserModel = get_user_model()


class BalanceSerializer(serializers.Serializer):
    user_from = serializers.ModelField(model_field=get_user_model()._meta.get_field('id'), required=True)
    users_to = serializers.MultipleChoiceField(choices=User.objects.filter(is_active=True).
                                               values_list('INN', 'username'), required=True)
    dec_sum = serializers.DecimalField(required=True, min_value=0, max_digits=8, decimal_places=2)

    def validate(self, attrs):
        try:
            user_from = UserModel.objects.get(pk=int(attrs.get('user_from')))
        except UserModel.DoesNotExist:
            raise exceptions.ValidationError(_('Укажите активного пользователя от которого перевод.'))

        if user_from.balance < attrs.get('dec_sum'):
            raise exceptions.ValidationError(_('Указанная сумма привышает допустимое значение ( %s )') % user_from.balance)

        users_to_list = attrs.get('users_to')
        if not len(users_to_list) > 0:
            raise exceptions.ValidationError(_('Выберите хотя бы одного пользователя которому перевод.'))
        elif len(users_to_list) != UserModel.objects.filter(INN__in=users_to_list).exclude(pk=user_from.id).count():
            raise exceptions.ValidationError(_('Укажите активных пользователей на которых будет перевод.'))

        return attrs

    def validate_dec_sum(self, value):
        if value <= 0:
            raise serializers.ValidationError('Указанная сумма должна быть больше нуля!')
        return value

    def update(self):
        with transaction.atomic():
            user_from = UserModel.objects.get(pk=int(self.validated_data['user_from']))
            user_from.balance = F('balance') - self.validated_data['dec_sum']
            user_from.save()
            users_to_list = self.validated_data['users_to']
            UserModel.objects.filter(INN__in=users_to_list).\
                update(balance=F('balance') + self.validated_data['dec_sum']/len(users_to_list))


class UserSerializer(serializers.ModelSerializer):
    inn = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'inn', 'balance')

    def get_inn(self, obj):
        return str(obj.INN)
