from django.urls import path
from .views import ModuleQuestionsView, SubmitQuizView

urlpatterns = [
    path('module/<int:module_id>/questions/', ModuleQuestionsView.as_view(), name='module-questions'),
    path('submit/', SubmitQuizView.as_view(), name='submit-quiz'),
]