from django.urls import path
from .views import AssignmentCreateView, AssignmentListView, AssignmentUnlockView, BulkAssignByLocationView

urlpatterns = [
    path('', AssignmentListView.as_view(), name='assignment-list'),
    path('create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('<int:assignment_id>/unlock/', AssignmentUnlockView.as_view(), name='assignment-unlock'),
    path('bulk-assign/', BulkAssignByLocationView.as_view(), name='bulk-assign-by-location'),
]