from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from course.models import SubModule,Module
from .serializers import SubModuleSerializer,SubModuleEditSerializer,SubModuleCreateSerializer
from core.permission import IsTenantAdmin,IsTenantActive
from course.views import DefaultPagination
from rest_framework.generics import GenericAPIView

class SubModule_View(GenericAPIView):
    permission_classes = [IsAuthenticated,IsTenantActive]
    pagination_class = DefaultPagination
    serializer_class = SubModuleSerializer

    def get_queryset(self):
        user = self.request.user

        if user.role == User.SUPER_ADMIN:
            return SubModule.objects.all()
        elif user.role == User.TENANT_ADMIN:
            return  SubModule.objects.filter(module__course__tenant = user.tenant)
        elif user.role == User.TENANT_USER:
            return SubModule.objects.filter(
                module__course__status = "PUBLISHED",
                module__course__enrollements__user = user
            )

    def get(self,request):
        query = self.get_queryset()
        page = self.paginate_queryset(query)
        serializer = self.get_serializer(page,many=True)
        return self.get_paginated_response(serializer.data)

class SubModule_Create(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def post(self,request):
        user = request.user
        if user.role != User.TENANT_ADMIN:
            return Response({"details": "Tenant Admin need to create submodule"},status = 403)
        module_id = request.data.get("module")
        if not module_id:
            return Response(
                {"detail": "Module ID is required"},
                status=403
            )
        try:
            module = Module.objects.get(
                id = module_id, 
                course__tenant = user.tenant
            )
        except Module.DoesNotExist:
            return Response({"details":"Module DB not found"},status=403)

        serializers = SubModuleCreateSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save(
                module = module
            )
            return Response(serializers.data,status=200)
        return Response(serializers.errors,status=403)

class SubModule_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]

    def put(self,request,pk):
        user = request.user
        try:
            submodule = SubModule.objects.get(pk = pk,module__course__tenant = user.tenant )
        except SubModule.DoesNotExist:
            return Response({"details":"primary key is not found "},status=403)
        
        serializer = SubModuleEditSerializer(submodule,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response({"details":"Error"},status=403)
    
    def delete(self,request,pk):
        tenant = request.user.tenant
        try:
            submodule = SubModule.objects.get(pk=pk,module__course__tenant = tenant)
        except SubModule.DoesNotExist:
            return Response({"details":"DB not found"})        
        submodule.delete()
        return Response({"details":"Deleted Successfully"},status=200)