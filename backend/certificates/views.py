from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Certificate
from .serializers import CertificateSerializer
from locations.models import UserLocation


class CertificateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "HR":
            certificates = Certificate.objects.all()

        elif user.role == "SUPER_ADMIN":
            location_ids = UserLocation.objects.filter(user=user).values_list('location_id', flat=True)
            certificates = Certificate.objects.filter(user__userlocation__location_id__in=location_ids).distinct()

        elif user.role == "ADMIN":
            location_ids = UserLocation.objects.filter(user=user).values_list('location_id', flat=True)
            certificates = Certificate.objects.filter(user__userlocation__location_id__in=location_ids).distinct()

        elif user.role == "EDUCATOR":
            certificates = Certificate.objects.filter(user=user)

        else:
            return Response({"detail": "Access denied"}, status=403)

        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)