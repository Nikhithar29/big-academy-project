from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Module
from .serializers import ModuleSerializer


class ModuleListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        modules = Module.objects.all().prefetch_related('steps')
        serializer = ModuleSerializer(modules, many=True)
        return Response(serializer.data)


class ModuleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, module_id):
        try:
            module = Module.objects.prefetch_related('steps').get(id=module_id)
        except Module.DoesNotExist:
            return Response({"detail": "Module not found"}, status=404)

        serializer = ModuleSerializer(module)
        return Response(serializer.data)