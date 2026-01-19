from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permission import UserRole
from course.models import VideoProgress,SubModule,Course_db
from .serializers import VideoProgress_Serializer


class Videoprogress_View(APIView):
    permission_classes =[IsAuthenticated]
    def get(self, request):
        user = request.user
       
        if user.role == UserRole.SUPER_ADMIN:
            data = VideoProgress.objects.all()
        elif user.role == UserRole.TENANT_ADMIN:
            data = VideoProgress.objects.select_related(
                 "user",
                 "submodule",
                 "submodule__module",
                 "submodule__module__course"
            ).filter(
              submodule__module__course__tenant = user.tenant,
             # user = user
            )
        elif user.role == UserRole.TENANT_USER:
            data = VideoProgress.objects.select_related(
                  "user",
                 "submodule",
                 "submodule__module",
                 "submodule__module__course"
            ).filter(
               submodule__module__course__status = "PUBLISHED",
               user = user
            )
        else:
            return Response({"details":"Access Denied"},status=403)
        
        serializer = VideoProgress_Serializer(data,many=True)
        return Response(serializer.data,status = 200)
    
    def post(self, request):
        user = request.user
        if user.role == UserRole.SUPER_ADMIN:
            return Response({"details":"super admin cannot post video progress"})
        
        submodule_id = request.data.get("submodule")
        last_duration = request.data.get("last_duration",0)
        try:
            submodule = SubModule.objects.get(
                    id = submodule_id,
                    module__course__tenant = user.tenant
                )
        except SubModule.DoesNotExist:
            return Response({"details":"submodule not found"},status = 403)
        
        if user.role == UserRole.TENANT_USER:
            enrolled_user = submodule.module.course.enrollements.filter(
                user = user
            ).exists()
            if not enrolled_user:
                return Response({"details":"User is not enrolled "},status=403)
        
        progress,created = VideoProgress.objects.update_or_create(
            user = user,
            submodule = submodule,
            defaults = {
                 "last_duration" : last_duration
            }
        )

        serializer = VideoProgress_Serializer(progress)
        return Response (serializer.data,status=200)
            

class Videoprogress_Edit(APIView):
    permission_classes = [IsAuthenticated]
    
    def put (self,request,pk):
        try:
             progress = VideoProgress.objects.get(pk=pk)
        except VideoProgress.DoesNotExist:
            return Response({"details":"VideoProgress data not found"},status= 403)
        
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Tenant Admin is required"},status=403)
         
        if(progress.submodule.module.course.tenant != user.tenant):
            return Response({"details":"Not Authorized"},status=403)

        serializer = VideoProgress_Serializer(progress,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"details":"Updated"},status=200)
        return Response({"details":"failed"},status=403)
    
    def delete(self,request,pk):
        try:
            progress = VideoProgress.objects.get(pk=pk)
        except VideoProgress.DoesNotExist:
            return Response({"details":"VideoProgress Data is not found "},status = 403)
        user = request.user
        if user.role != UserRole.TENANT_ADMIN:
            return Response({"details":"Tenant Admin is required"},status=403)
        if(progress.submodule.module.course.tenant != user.tenant):
            return Response({"details":"Not Authroized "},status=403)
        
        progress.delete()
        return Response({"details":"Deleted Successfully"},status=200)
        



            
        
            


            




