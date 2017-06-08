from django.conf.urls import url
from django.views.generic.base import TemplateView

from .views import BalanceView, UserViewSet


urlpatterns = [
    url(r'^post/$', BalanceView.as_view(), name='transfer'),
    url(r'^users/list/$', UserViewSet.as_view({'get': 'list'}), name='users'),
    url(r'^$', TemplateView.as_view(template_name="transfer.html"), name='index-transfer'),
]
