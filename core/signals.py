from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import AccessExceptionRequest, AccessRequestAuditLog


@receiver(pre_save, sender=AccessExceptionRequest)
def log_changes(sender, instance, **kwargs):
    if not instance.pk:
        return  # new object, nothing to compare

    old = AccessExceptionRequest.objects.get(pk=instance.pk)

    fields_to_track = [
        "status",
        "reason",
        "reviewer_upn",
        "policy_category",
    ]

    for field in fields_to_track:
        old_value = getattr(old, field)
        new_value = getattr(instance, field)

        if old_value != new_value:
            AccessRequestAuditLog.objects.create(
                request=instance,
                changed_by=instance.reviewer_upn or "system",
                field_name=field,
                old_value=str(old_value),
                new_value=str(new_value),
            )
