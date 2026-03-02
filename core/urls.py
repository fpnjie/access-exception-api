from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccessExceptionRequestViewSet

router = DefaultRouter()
router.register("requests", AccessExceptionRequestViewSet, basename="access-request")

urlpatterns = [
    path("", include(router.urls)),
]
