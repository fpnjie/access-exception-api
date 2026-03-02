from django.db import models
from django.utils import timezone
import random
from django.core.validators import RegexValidator


class AccessParameters(models.Model):
    country_code = models.CharField(
        max_length=2,
        blank=True,
        null=True,
        validators=[RegexValidator(r"^[A-Z]{2}$", "Use a 2-letter uppercase country code (e.g. US, GB).")],
        help_text="2-letter ISO country code (e.g. US, GB)",
    )
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()
    require_compliant_device = models.BooleanField(default=False)
    mfa_method_required = models.CharField(max_length=100)

    def __str__(self):
        return f"Params {self.id}"


class AccessExceptionRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
        ("Expired", "Expired"),
    ]

    POLICY_CATEGORIES = [
        ("Geofence", "Geofence"),
        ("Device_Compliance", "Device Compliance"),
        ("MFA_Override", "MFA Override"),
        ("Other", "Other"),
    ]

    request_id = models.CharField(max_length=50, unique=True, blank=True)
    user_principal_name = models.EmailField()
    policy_category = models.CharField(
        max_length=50,
        choices=POLICY_CATEGORIES,
        default="Other",
    )
    parameters = models.OneToOneField(
        AccessParameters,
        on_delete=models.CASCADE,
        related_name="request",
    )
    approval_id = models.CharField(max_length=50, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    reason = models.TextField(blank=True, null=True)
    reviewer_upn = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def generate_request_id() -> str:
        """Generate an ID like 435-099."""
        return f"{random.randint(0, 999):03d}-{random.randint(0, 999):03d}"

    def save(self, *args, **kwargs):
        # Autopopulate request_id if missing, while ensuring uniqueness.
        if not self.request_id:
            for _ in range(25):
                candidate = self.generate_request_id()
                if not AccessExceptionRequest.objects.filter(request_id=candidate).exists():
                    self.request_id = candidate
                    break
            else:
                raise RuntimeError("Unable to generate a unique request_id")

        super().save(*args, **kwargs)

    def auto_expire(self):
        if self.status not in ["Expired", "Rejected"]:
            if timezone.now() > self.parameters.end_timestamp:
                self.status = "Expired"
                self.save()

    def __str__(self):
        return self.request_id


class AccessRequestAuditLog(models.Model):
    request = models.ForeignKey(
        AccessExceptionRequest,
        on_delete=models.CASCADE,
        related_name="audit_logs",
    )
    changed_by = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"AuditLog {self.id} for {self.request.request_id}"
