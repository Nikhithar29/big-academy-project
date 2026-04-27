from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from assignments.models import Assignment
from certificates.models import Certificate
from locations.models import UserLocation
from modules_app.models import Module
from users.models import CustomUser


class EducatorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "EDUCATOR":
            return Response({"detail": "Access denied"}, status=403)

        assignments_data = []
        assignments = Assignment.objects.filter(user=request.user).select_related('module', 'location')
        for a in assignments:
            assignments_data.append({
                "id": a.id,
                "module": a.module.title,
                "location": a.location.name,
                "status": a.status,
                "attempts_used": a.attempts_used,
            })

        certificates_data = []
        certificates = Certificate.objects.filter(user=request.user).select_related('module')
        for c in certificates:
            certificates_data.append({
                "id": c.id,
                "module": c.module.title,
                "certificate_id": c.certificate_id,
                "issued_at": c.issued_at,
            })

        return Response({
            "user": request.user.email,
            "role": request.user.role,
            "assignments": assignments_data,
            "certificates": certificates_data,
        })


class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "ADMIN":
            return Response({"detail": "Access denied"}, status=403)

        user_location_links = UserLocation.objects.filter(user=request.user).select_related('location')
        location_ids = user_location_links.values_list('location_id', flat=True)

        locations_data = [{"location": ul.location.name} for ul in user_location_links]

        users_data = []
        users_in_location = CustomUser.objects.filter(
            userlocation__location_id__in=location_ids
        ).distinct()
        for u in users_in_location:
            users_data.append({
                "id": u.id,
                "email": u.email,
                "role": u.role,
                "status": u.status,
            })

        assignments_data = []
        assignments_in_location = Assignment.objects.filter(
            location_id__in=location_ids
        ).select_related('user', 'module', 'location')
        for a in assignments_in_location:
            assignments_data.append({
                "id": a.id,
                "user": a.user.email,
                "module": a.module.title,
                "location": a.location.name,
                "status": a.status,
                "attempts_used": a.attempts_used,
            })

        return Response({
            "user": request.user.email,
            "role": request.user.role,
            "locations": locations_data,
            "users": users_data,
            "assignments": assignments_data,
        })


class SuperAdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "SUPER_ADMIN":
            return Response({"detail": "Access denied"}, status=403)

        user_location_links = UserLocation.objects.filter(user=request.user).select_related('location')
        location_ids = user_location_links.values_list('location_id', flat=True)

        locations_data = [{"location": ul.location.name} for ul in user_location_links]

        users_data = []
        users_in_locations = CustomUser.objects.filter(
            userlocation__location_id__in=location_ids
        ).distinct()
        for u in users_in_locations:
            users_data.append({
                "id": u.id,
                "email": u.email,
                "role": u.role,
                "status": u.status,
            })

        assignments_data = []
        assignments_in_locations = Assignment.objects.filter(
            location_id__in=location_ids
        ).select_related('user', 'module', 'location')
        for a in assignments_in_locations:
            assignments_data.append({
                "id": a.id,
                "user": a.user.email,
                "module": a.module.title,
                "location": a.location.name,
                "status": a.status,
                "attempts_used": a.attempts_used,
            })

        modules_data = []
        for m in Module.objects.all():
            modules_data.append({
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "created_at": m.created_at,
            })

        return Response({
            "user": request.user.email,
            "role": request.user.role,
            "locations": locations_data,
            "users": users_data,
            "assignments": assignments_data,
            "modules": modules_data,
        })


class HRDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "HR":
            return Response({"detail": "Access denied"}, status=403)

        users_data = []
        for u in CustomUser.objects.all():
            users_data.append({
                "id": u.id,
                "email": u.email,
                "role": u.role,
                "status": u.status,
            })

        modules_data = []
        for m in Module.objects.all():
            modules_data.append({
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "created_at": m.created_at,
            })

        assignments_data = []
        for a in Assignment.objects.select_related('user', 'module', 'location').all():
            assignments_data.append({
                "id": a.id,
                "user": a.user.email,
                "module": a.module.title,
                "location": a.location.name,
                "status": a.status,
                "attempts_used": a.attempts_used,
            })

        return Response({
            "user": request.user.email,
            "role": request.user.role,
            "users": users_data,
            "modules": modules_data,
            "assignments": assignments_data,
        })
