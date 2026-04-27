from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from modules_app.models import Module
from assignments.models import Assignment
from .models import Question
from .serializers import QuestionSerializer, QuizAttemptSerializer
from .services import submit_quiz


class ModuleQuestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, module_id):
        user = request.user

        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({"detail": "Module not found"}, status=404)

        if user.role == "EDUCATOR":
            has_assignment = Assignment.objects.filter(user=user, module=module).exists()
            if not has_assignment:
                return Response({"detail": "You are not assigned to this module"}, status=403)

        questions = Question.objects.filter(module=module).prefetch_related('choices')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class SubmitQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        module_id = request.data.get("module_id")
        submitted_answers = request.data.get("answers", {})

        if not module_id:
            return Response({"detail": "module_id is required"}, status=400)

        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response({"detail": "Module not found"}, status=404)

        if user.role != "EDUCATOR":
            return Response({"detail": "Only educators can submit quizzes"}, status=403)

        if not Assignment.objects.filter(user=user, module=module).exists():
            return Response({"detail": "You are not assigned to this module"}, status=403)

        try:
            attempt = submit_quiz(user, module, submitted_answers)
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)
        except Exception as e:
            return Response({"detail": f"Submission failed: {str(e)}"}, status=400)

        serializer = QuizAttemptSerializer(attempt)
        return Response(serializer.data, status=status.HTTP_200_OK)