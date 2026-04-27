from rest_framework import serializers
from .models import Assignment


class AssignmentSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = Assignment
        fields = [
            'id',
            'user',
            'user_email',
            'module',
            'module_title',
            'location',
            'location_name',
            'assigned_by',
            'assigned_at',
            'status',
            'attempts_used',
        ]
        read_only_fields = ['assigned_by', 'assigned_at', 'status', 'attempts_used']