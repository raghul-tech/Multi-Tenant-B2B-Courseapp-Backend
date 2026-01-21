from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole,IsTenantAdmin
from .models import Skills
from rest_framework.response import Response
from .serializers import Skills_View_Serializers,Skills_Create_Serializers,Skills_Edit_Serializers

# Create your views here.
class Skills_View(APIView):
    permission_classes = [IsAuthenticated]
    def get_queryset(self,user):
        if user.role == UserRole.SUPER_ADMIN:
            return Skills.objects.all()
        else:
            return Skills.objects.filter(tenant = user.tenant)
        
    def get(self,request):
        data = self.get_queryset(request.user)
        serializer = Skills_View_Serializers(data,many=True)
        return Response(serializer.data,status=200)
    
class Skills_Create(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def post(self,request):
        serializer = Skills_Create_Serializers(
            data = request.data,
            context = {"request":request}
            )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=201)
    
    
class Skills_Edit(APIView):
    permission_classes = [IsAuthenticated,IsTenantAdmin]
    def put (self,request,pk):
        user = request.user      
        try:
            skills = Skills.objects.get(
                pk = pk,
                tenant = user.tenant)
        except Skills.DoesNotExist:
            return Response({"details":"No data found "},status=403)
        
        serializer = Skills_Edit_Serializers(skills,data = request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=200)
        return Response(serializer.errors,status=403)
        
    def delete(self,request,pk):
        user = request.user
        try:
            skills = Skills.objects.get(
                pk = pk,
                tenant = user.tenant)
        except Skills.DoesNotExist:
            return Response({"details":"No data found "},status=403)
        
        skills.delete()
        return Response({"details":"Skill deleted"},status=200)