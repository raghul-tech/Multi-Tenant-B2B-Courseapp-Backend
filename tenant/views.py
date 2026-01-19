
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import TenantSerializer
from .models import Tenant
from core.permission import  IsSuperAdmin

# Create your views here.
class TenantDashboard(APIView):
    permission_classes = [IsAuthenticated,IsSuperAdmin]

    def get(self, request):
      try:
            tenant = Tenant.objects.all()
            serializer = TenantSerializer(tenant , many=True)
            return Response(serializer.data,status=200)
      except Tenant.DoesNotExist:
            return Response({"detail": "Tenant does not exist."}, status=403)
      
    def post(self, request):
        
        serializer = TenantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, pk):
        try:
            tenant = Tenant.objects.get(pk=pk)
        except Tenant.DoesNotExist:
            return Response({"detail": "Tenant not found."}, status=404)

        serializer = TenantSerializer(tenant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    
    def delete(self, request, pk):

        try:
            tenant = Tenant.objects.get(pk=pk)
        except Tenant.DoesNotExist:
            return Response({"detail": "Tenant not found."}, status=404)
        tenant.delete()
        return Response({"detail": "Tenant deleted successfully."}, status=204)