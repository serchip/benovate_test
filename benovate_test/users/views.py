from django.utils.translation import ugettext as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import BalanceSerializer, UserSerializer
from .models import User


class BalanceView(GenericAPIView):

    serializer_class = BalanceSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {'success': False,
                 'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.update()
        return Response(
            {
                "success": True,
                'message': _('Успешное сохранение!')
            },
            status=status.HTTP_200_OK
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer