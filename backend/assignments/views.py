from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Assignment
from .serializers import AssignmentSerializer
from .services import unlock_assignment
from locations.models import UserLocation
from users.models import CustomUser


class AssignmentCreateView(generics.CreateAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(assigned_by=self.request.user)


class AssignmentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "HR":
            assignments = Assignment.objects.all()

        elif user.role in ["SUPER_ADMIN", "ADMIN"]:
            location_ids = UserLocation.objects.filter(user=user).values_list('location_id', flat=True)
            assignments = Assignment.objects.filter(location_id__in=location_ids)

        elif user.role == "EDUCATOR":
            assignments = Assignment.objects.filter(user=user)

        else:
            return Response({"detail": "Access denied"}, status=403)

        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)


class AssignmentUnlockView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, assignment_id):
        user = request.user

        try:
            assignment = Assignment.objects.select_related('location').get(id=assignment_id)
        except Assignment.DoesNotExist:
            return Response({"detail": "Assignment not found"}, status=404)

        if user.role == "HR":
            pass

        elif user.role in ["ADMIN", "SUPER_ADMIN"]:
            allowed_location_ids = UserLocation.objects.filter(user=user).values_list('location_id', flat=True)
            if assignment.location_id not in allowed_location_ids:
                return Response({"detail": "Access denied for this location"}, status=403)

        else:
            return Response({"detail": "Access denied"}, status=403)

        unlocked = unlock_assignment(assignment_id)

        return Response({
            "message": "Assignment unlocked successfully",
            "assignment": {
                "id": unlocked.id,
                "user": unlocked.user.email,
                "module": unlocked.module.title,
                "location": unlocked.location.name,
                "status": unlocked.status,
                "attempts_used": unlocked.attempts_used,
            }
        }, status=status.HTTP_200_OK)


class BulkAssignByLocationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        location_id = request.data.get("location_id")
        module_id = request.data.get("module_id")

        if not location_id or not module_id:
            return Response(
                {"detail": "location_id and module_id are required"},
                status=400
            )

        if user.role == "HR":
            allowed = True

        elif user.role in ["ADMIN", "SUPER_ADMIN"]:
            allowed_location_ids = UserLocation.objects.filter(user=user).values_list('location_id', flat=True)
            allowed = int(location_id) in allowed_location_ids

        else:
            return Response({"detail": "Access denied"}, status=403)

        if not allowed:
            return Response({"detail": "You cannot assign to this location"}, status=403)

        educator_ids = UserLocation.objects.filter(
            location_id=location_id,
            user__role="EDUCATOR"
        ).values_list('user_id', flat=True)

        created_assignments = []
        skipped_users = []

        for educator_id in educator_ids:
            existing = Assignment.objects.filter(
                user_id=educator_id,
                module_id=module_id,
                location_id=location_id
            ).first()

            if existing:
                skipped_users.append(educator_id)
                continue

            assignment = Assignment.objects.create(
                user_id=educator_id,
                module_id=module_id,
                location_id=location_id,
                assigned_by=user
            )

            created_assignments.append({
                "id": assignment.id,
                "user_id": assignment.user_id,
                "module_id": assignment.module_id,
                "location_id": assignment.location_id,
                "status": assignment.status,
            })

        return Response({
            "message": "Bulk assignment completed",
            "created_count": len(created_assignments),
            "skipped_count": len(skipped_users),
            "created_assignments": created_assignments,
            "skipped_user_ids": skipped_users,
        }, status=200)