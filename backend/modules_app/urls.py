from django.urls import path
from .views import ModuleListView, ModuleDetailView

urlpatterns = [
    path('', ModuleListView.as_view(), name='module-list'),
    path('<int:module_id>/', ModuleDetailView.as_view(), name='module-detail'),
]