from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from skills.models import CourseSkill
from core.permission import UserRole,IsTenantAdmin
from rest_framework.response import Response
from .serializers import CourseSkill_View_Serializer,CourseSkill_Create_Serializer,CourseSkill_Edit_Serializer


class CourseSkill_View(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self,user):
        if user.role == UserRole.SUPER_ADMIN:
            return CourseSkill.objects.all()
        else:
            return CourseSkill.objects.filter(tenant = user.tenant)
        
    def get(self,request):
        data = self.get_queryset(request.user)
        serializer = CourseSkill_View_Serializer(data,many=True)
        return Response(serializer.data,status=200)

class CourseSkill_Create(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def post(self,request):
        data = CourseSkill_Create_Serializer(
            data = request.data,
            context = { 
                "request":request
            }
        )
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data.data,status=201)

class CourseSkill_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def get_queryset(self,pk,user):
            data = CourseSkill.objects.get(
                pk=pk,
                tenant = user.tenant
                )
            return data

    def put (self,request,pk):
        try:
            data = self.get_queryset(pk,request.user)
        except CourseSkill.DoesNotExist:
            return Response({"details":"course skill is not there "},status=403)
        serializer = CourseSkill_Edit_Serializer(data,data=request.data,partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data,status=200)
    
    def delete(self,request,pk):
        try:
           data = self.get_queryset(pk,request.user)
        except CourseSkill.DoesNotExist:
            return Response({"details":"course skill is not there "},status=403)
        data.delete()
        return Response({"details":"deleted successfully"},status=200)





        


        



