from django.contrib import admin
from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'module', 'location', 'status', 'attempts_used', 'assigned_by', 'assigned_at')
    list_filter = ('status', 'location')
    search_fields = ('user__email', 'module__title', 'location__name')