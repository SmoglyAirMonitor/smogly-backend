from django.conf.urls import url, include
from rest_framework import routers

from .views import StationViewSet, MeteringViewSet, schema_view, ObtainJWT

router = routers.DefaultRouter()
router.register(r'station', StationViewSet)
router.register(r'metering', MeteringViewSet)

urlpatterns = (
    # urls for Django Rest Framework API
    url(r'^api/v1/', include(router.urls)),
    url(r'^api/v1/api-token-auth/', ObtainJWT.as_view(), name='api-token-auth'),
    url(r'^api/v1/docs/',  schema_view),
)
