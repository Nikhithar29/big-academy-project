from rest_framework import serializers
from .models import Question, AnswerChoice, QuizAttempt, QuizAnswer


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'option_text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'choices']


class QuizAnswerSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    selected_option_text = serializers.CharField(source='selected_option.option_text', read_only=True)

    class Meta:
        model = QuizAnswer
        fields = ['id', 'question', 'question_text', 'selected_option', 'selected_option_text', 'is_correct']


class QuizAttemptSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    module_title = serializers.CharField(source='module.title', read_only=True)
    answers = QuizAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = QuizAttempt
        fields = [
            'id',
            'user',
            'user_email',
            'module',
            'module_title',
            'score',
            'passed',
            'attempt_number',
            'created_at',
            'answers',
        ]