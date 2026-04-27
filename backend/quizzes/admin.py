from django.contrib import admin
from .models import Question, AnswerChoice, QuizAttempt, QuizAnswer

admin.site.register(Question)
admin.site.register(AnswerChoice)
admin.site.register(QuizAttempt)
admin.site.register(QuizAnswer)