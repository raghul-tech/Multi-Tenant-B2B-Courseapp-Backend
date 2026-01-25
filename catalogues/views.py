from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permission import UserRole
from .models import Catalogues
from .serializers import Catalogues_Serializers,Catalogues_Details_Serializers

# Create your views here.

class Catalogues_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.role == UserRole.SUPER_ADMIN:
            data = Catalogues.objects.all()
        elif user.role == (UserRole.TENANT_ADMIN or UserRole.TENANT_USER):
            data = Catalogues.objects.filter(tenant = user.tenant)
        else:
            return Response({"details":"not authorized"},status=403)
        
        serializer = Catalogues_Serializers(data,many=True)
        return Response(serializer.data,status=200)
    
    def post(self,request):
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Tenant Admin can only create catalogues"},status=403)
        catalog, created =  Catalogues.objects.get_or_create(
                name = request.data.get("name"),
                 created_by = user,
                tenant = user.tenant
            )
        if created:
             serializer = Catalogues_Serializers(catalog)
             return Response(serializer.data,status=200)
        return Response({"details":"can't create catalogue"},status=403)


class Catalogues_Edit(APIView):
    permission_classes = [IsAuthenticated]

    def put(self,request,pk):
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Only Tenant Admin can make changes"},status=403)
        try:
            catalog = Catalogues.objects.get(pk=pk)
        except Catalogues.DoesNotExist:
            return Response({"details":"Catalog is not found"},status=403)
        if catalog.tenant != user.tenant:
            return Response({"details":"Tenant can change only their Catalogous"})

        serializer = Catalogues_Serializers(catalog,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=403)
    
    def delete(self,request,pk):
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Only Tenant Admin can make changes"},status=403)
        try:
            catalog = Catalogues.objects.get(pk=pk)
        except Catalogues.DoesNotExist:
            return Response({"details":"Catalog is not found"},status=403)
        if catalog.tenant != user.tenant:
            return Response({"details":"Tenant can change only their Catalogous"})
        catalog.delete()
        return Response({"details":"catalogue deleted successfully"},status=200)
         
class Catalogues_Details(APIView):
    permission_classes = [IsAuthenticated]
    def get(self ,request):
        user = request.user
        if user.role == UserRole.SUPER_ADMIN:
            data = Catalogues.objects.all()
        elif user.role == (UserRole.TENANT_ADMIN or UserRole.TENANT_USER):
            data = Catalogues.objects.filter(tenant = user.tenant)
        else:
            return Response({"details":"not authorized"},status=403)     
        serializer = Catalogues_Details_Serializers(data,many=True)
        return Response(serializer.data,status=200)

