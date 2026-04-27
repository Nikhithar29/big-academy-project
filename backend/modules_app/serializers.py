from rest_framework import serializers
from .models import Module, ModuleStep


class ModuleStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleStep
        fields = ['id', 'title', 'content_type', 'content_url', 'order_number']


class ModuleSerializer(serializers.ModelSerializer):
    steps = ModuleStepSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'created_at', 'steps']