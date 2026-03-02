from rest_framework import serializers
from .models import AccessExceptionRequest, AccessParameters, AccessRequestAuditLog


class AccessParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessParameters
        fields = '__all__'

    def to_internal_value(self, data):
        # Normalize before model field validators run (e.g. regex for uppercase).
        if isinstance(data, dict) and "country_code" in data and isinstance(data.get("country_code"), str):
            data = {**data, "country_code": data["country_code"].strip().upper()}
        return super().to_internal_value(data)

    def validate_country_code(self, value: str) -> str:
        value = (value or "").strip().upper()
        if len(value) != 2 or not value.isalpha():
            raise serializers.ValidationError("Use a 2-letter country code like 'US' or 'GB'.")
        return value


class AccessRequestAuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequestAuditLog
        fields = ["timestamp", "changed_by", "field_name", "old_value", "new_value"]


class AccessExceptionRequestSerializer(serializers.ModelSerializer):
    parameters = AccessParametersSerializer()
    audit_logs = AccessRequestAuditLogSerializer(many=True, read_only=True)
    request_id = serializers.CharField(read_only=True)
    policy_category = serializers.ChoiceField(choices=AccessExceptionRequest.POLICY_CATEGORIES, required=False)
    approval_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = AccessExceptionRequest
        fields = [
            "request_id",
            "user_principal_name",
            "policy_category",
            "parameters",
            "approval_id",
            "status",
            "reason",
            "reviewer_upn",
            "created_at",
            "updated_at",
            "audit_logs",
        ]

    def create(self, validated_data):
        params_data = validated_data.pop("parameters")
        params = AccessParameters.objects.create(**params_data)
        return AccessExceptionRequest.objects.create(parameters=params, **validated_data)

    def update(self, instance, validated_data):
        params_data = validated_data.pop("parameters", None)

        if params_data:
            for key, value in params_data.items():
                setattr(instance.parameters, key, value)
            instance.parameters.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        instance.auto_expire()
        return instance
