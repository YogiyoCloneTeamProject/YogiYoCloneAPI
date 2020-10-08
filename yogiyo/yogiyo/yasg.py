from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf.urls import url
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="yogiyo API",
        default_version='v1',
        description="http://52.79.251.125/ aws server dns",
        terms_of_service="http://52.79.251.125/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns_yasg = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
