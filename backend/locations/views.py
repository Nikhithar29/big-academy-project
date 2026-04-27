from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Location, UserLocation
from .serializers import LocationSerializer


class LocationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "HR":
            locations = Location.objects.all()

        elif user.role in ["ADMIN", "SUPER_ADMIN", "EDUCATOR"]:
            location_ids = UserLocation.objects.filter(user=user).values_list('location_id', flat=True)
            locations = Location.objects.filter(id__in=location_ids)

        else:
            return Response({"detail": "Access denied"}, status=403)

        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)