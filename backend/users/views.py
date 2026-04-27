from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions

from .models import CustomUser
from .serializers import UserSerializer, UserCreateUpdateSerializer
from locations.models import UserLocation


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if user.role == "HR":
            users = CustomUser.objects.all()

        elif user.role in ["ADMIN", "SUPER_ADMIN"]:
            location_ids = UserLocation.objects.filter(user=user).values_list('location_id', flat=True)
            users = CustomUser.objects.filter(
                userlocation__location_id__in=location_ids
            ).distinct()

        else:
            return Response({"detail": "Access denied"}, status=403)

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if request.user.role != "HR":
            return Response({"detail": "Only HR can create users"}, status=403)
        return super().create(request, *args, **kwargs)


class UserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if request.user.role != "HR":
            return Response({"detail": "Only HR can update users"}, status=403)
        return super().update(request, *args, **kwargs)