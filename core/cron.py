from django.utils import timezone
from .models import AccessExceptionRequest


def expire_requests():
    now = timezone.now()
    qs = AccessExceptionRequest.objects.filter(status="Approved")
    for req in qs:
        if req.parameters.end_timestamp < now:
            req.status = "Expired"
            req.save()
