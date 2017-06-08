from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='balance:index-transfer', permanent=False), name='index'),

    url(r'^balance/', include('users.urls', namespace="balance")),


    # admin urls
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^admin/django-ses/', include('django_ses.urls'))
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
