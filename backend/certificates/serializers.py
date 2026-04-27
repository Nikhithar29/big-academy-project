from rest_framework import serializers
from .models import Certificate


class CertificateSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)

    class Meta:
        model = Certificate
        fields = ['id', 'user', 'user_email', 'module', 'module_title', 'certificate_id', 'issued_at']