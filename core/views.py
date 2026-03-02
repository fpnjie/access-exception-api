from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import AccessExceptionRequest
from .serializers import AccessExceptionRequestSerializer
from .permissions import IsReviewer


class AccessExceptionRequestViewSet(viewsets.ModelViewSet):
    queryset = AccessExceptionRequest.objects.all().order_by("-created_at")
    serializer_class = AccessExceptionRequestSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["status", "user_principal_name", "policy_category"]

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [IsReviewer()]
        return [IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        for req in qs:
            req.auto_expire()
        return qs
