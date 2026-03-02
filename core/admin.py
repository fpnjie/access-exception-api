from django.contrib import admin
from .models import AccessExceptionRequest, AccessParameters, AccessRequestAuditLog


@admin.register(AccessParameters)
class AccessParametersAdmin(admin.ModelAdmin):
    list_display = ("id", "start_timestamp", "end_timestamp", "require_compliant_device")


@admin.register(AccessExceptionRequest)
class AccessExceptionRequestAdmin(admin.ModelAdmin):
    list_display = (
        "request_id",
        "user_principal_name",
        "policy_category",
        "status",
        "reviewer_upn",
        "created_at",
    )
    list_filter = ("status", "policy_category")
    search_fields = ("request_id", "user_principal_name", "approval_id")


@admin.register(AccessRequestAuditLog)
class AccessRequestAuditLogAdmin(admin.ModelAdmin):
    list_display = ("request", "field_name", "changed_by", "timestamp")
    list_filter = ("field_name", "changed_by")
