from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import User
from course.models import SubModule,Module
from .serializers import SubModuleSerializer
from core.permission import IsTenantAdmin

class SubModule_View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user

        if user.role == User.SUPER_ADMIN:
            data = SubModule.objects.all()
        elif user.role == User.TENANT_ADMIN:
            data = SubModule.objects.filter(module__course__tenant = user.tenant)
        elif user.role == User.TENANT_USER:
            data = SubModule.objects.filter(
                module__course__status = "PUBLISHED",
                module__course__enrollements__user = user
            ).distinct()
        else:
            return Response({"details":"dont have access"},status = 403)
        
        serializers = SubModuleSerializer(data,many=True)
        return Response(serializers.data,status=200)
    
    def post(self,request):
        user = request.user

        if user.role != User.TENANT_ADMIN:
            return Response({"details": "Tenant Admin need to create submodule"},status = 403)
        

        module_id = request.data.get("modules")
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

        serializers = SubModuleSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save(
                module = module
            )
            return Response(serializers.data,status=200)
        return Response({"details":"Their was a error "},status=403)

class SubModule_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]

    def put(self,request,pk):
        try:
            submodule = SubModule.objects.get(pk = pk)
        except SubModule.DoesNotExist:
            return Response({"details":"primary key is not found "},status=403)
        
        user = request.user
        if user.role != User.TENANT_ADMIN:
            return Response({"details":"tenant admin required to create submodule"},status=403)
        if(submodule.module.course.tenant != user.tenant):
                return Response({"details":"dont have access"},status=403)
        
        serializer = SubModuleSerializer(submodule,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response({"details":"Error"},status=403)
    
    def delete(self,request,pk):
        try:
            submodule = SubModule.objects.get(pk=pk)
        except SubModule.DoesNotExist:
            return Response({"details":"DB not found"})
        user = request.user
        if user.role == User.SUPER_ADMIN:
            pass
        elif user.role == User.TENANT_ADMIN:
            if(submodule.module.course.tenant != user.tenant):
                return Response({"details":"dont have access"},status=403)
        else:
            return Response({"details":"dont have access"},status=403)
        
        submodule.delete()
        return Response({"details":"Deleted Successfully"},status=200)