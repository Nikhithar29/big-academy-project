from quizzes.models import QuizAttempt, QuizAnswer, Question, AnswerChoice
from assignments.models import Assignment
from certificates.services import generate_certificate


def submit_quiz(user, module, submitted_answers):
    """
    submitted_answers format:
    {
        "1": 2,
        "2": 5
    }
    or
    {
        1: 2,
        2: 5
    }
    """

    assignment = Assignment.objects.get(user=user, module=module)

    if assignment.status == 'LOCKED':
        raise ValueError("This module is locked.")

    if assignment.status == 'COMPLETED':
        raise ValueError("This module has already been completed.")

    questions = Question.objects.filter(module=module)
    total_questions = questions.count()

    if total_questions == 0:
        raise ValueError("No questions found for this module.")

    correct_count = 0
    next_attempt_number = assignment.attempts_used + 1

    attempt = QuizAttempt.objects.create(
        user=user,
        module=module,
        score=0,
        passed=False,
        attempt_number=next_attempt_number
    )

    for question in questions:
        selected_option_id = submitted_answers.get(str(question.id))
        if selected_option_id is None:
            selected_option_id = submitted_answers.get(question.id)

        if not selected_option_id:
            continue

        selected_option = AnswerChoice.objects.get(id=selected_option_id, question=question)
        is_correct = selected_option.is_correct

        if is_correct:
            correct_count += 1

        QuizAnswer.objects.create(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
            is_correct=is_correct
        )

    score = (correct_count / total_questions) * 100
    passed = score == 100

    attempt.score = score
    attempt.passed = passed
    attempt.save()

    assignment.attempts_used += 1

    if passed:
        assignment.status = 'COMPLETED'
        assignment.save()
        generate_certificate(user, module)
    else:
        if assignment.attempts_used >= 3:
            assignment.status = 'LOCKED'
        else:
            assignment.status = 'IN_PROGRESS'
        assignment.save()

    return attempt