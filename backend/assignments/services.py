from assignments.models import Assignment


def unlock_assignment(assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    assignment.status = "NOT_STARTED"
    assignment.attempts_used = 0
    assignment.save()
    return assignment