from django.urls import path
from .views import (
    EducatorDashboardView,
    AdminDashboardView,
    SuperAdminDashboardView,
    HRDashboardView,
)

urlpatterns = [
    path('educator/', EducatorDashboardView.as_view(), name='educator-dashboard'),
    path('admin/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('superadmin/', SuperAdminDashboardView.as_view(), name='superadmin-dashboard'),
    path('hr/', HRDashboardView.as_view(), name='hr-dashboard'),
]