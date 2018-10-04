from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework.authtoken import views as authtoken_views

from rest_framework import routers

from logocdn.views import LogoViewSet 


router = routers.DefaultRouter()
router.register(r'api/v1/logoentries', LogoViewSet, base_name='logoentries')


urlpatterns = router.urls