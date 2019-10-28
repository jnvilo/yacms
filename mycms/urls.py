from django.contrib import admin
from django.urls import path, re_path, include


from rest_framework import permissions
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from mycms import views
from mycms import api


schema_view = get_schema_view(
    openapi.Info(
        title="MyCMSProject API",
        default_version="v1",
        description="API for MyCMSProject Pages",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="admin@mycmsproject.org"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
router.register(r"node", api.NodeViewSet)
# router.register(r'api/v1/page', api.PageViewSet, base_name='page')


from mycms.pages import PageRegistry

PageRegistry.build_router_urls(router)
# urlpatterns = router.urls + urlpatterns

urlpatterns = [
    re_path(r"^api/v1/", include((router.urls, "mycms"))),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    re_path(r"^(?P<path>[-/\.a-z\d_]*)/$", views.PageView.as_view(), name="page"),
    re_path(r"^$", views.PageView.as_view(), name="page"),
]
