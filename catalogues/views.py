from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.permission import UserRole
from .models import Catalogues
from .serializers import Catalogues_Serializers,Catalogues_Details_Serializers
from core.permission import IsTenantAdmin,IsTenantActive
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView


# Create your views here.
class DefaultPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 50


class Catalogues_View(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = Catalogues_Serializers
    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.SUPER_ADMIN:
            return Catalogues.objects.all()
        elif user.role == UserRole.TENANT_ADMIN or UserRole.TENANT_USER:
            return Catalogues.objects.filter(tenant = user.tenant)

    def get(self, request):
        query = self.get_queryset()
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)

class Catalogues_Create(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def post(self,request):
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Tenant Admin can only create catalogues"},status=403)
        try:
            name = request.data.get('name')
        except:
            return Response({"details":"name is required"},status=403)
        catalog, created =  Catalogues.objects.get_or_create(
                name = name,
                 created_by = user,
                tenant = user.tenant
            )
        if created:
             serializer = Catalogues_Serializers(catalog)
             return Response(serializer.data,status=200)
        return Response({"details":"can't create catalogue"},status=403)


class Catalogues_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]

    def put(self,request,pk):
        user = request.user
        try:
            catalog = Catalogues.objects.get(pk=pk,tenant = user.tenant)
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
        try:
            catalog = Catalogues.objects.get(pk=pk,tenant = user.tenant)
        except Catalogues.DoesNotExist:
            return Response({"details":"Catalog is not found"},status=403)
        if catalog.tenant != user.tenant:
            return Response({"details":"Tenant can change only their Catalogous"})
        catalog.delete()
        return Response({"details":"catalogue deleted successfully"},status=200)
         
class Catalogues_Details(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = Catalogues_Details_Serializers
    def get_queryset(self):
        user = self.request.user
        if user.role == UserRole.SUPER_ADMIN:
            return Catalogues.objects.all()
        elif user.role == UserRole.TENANT_ADMIN or UserRole.TENANT_USER:
            return Catalogues.objects.filter(tenant = user.tenant)

    def get(self, request):
        query = self.get_queryset()
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)


