from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from course.models import Course_db
from core.permission import UserRole
from enrollement.models import Enrollement
from .models import Transactions
from .serializers import TransactionSerializers


# Create your views here.

class Transaction_Initialize(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
     
        user = request.user
        if user.role != UserRole.TENANT_USER:
            return Response({"details":"tenant user can only pay"},status=403)
        
        course_id = request.data.get("course")
        if not course_id:
            return Response({"details":"course id is required"},status = 403)
        try:
            course = Course_db.objects.get(
                id = course_id,
                tenant = user.tenant
                )
        except Course_db.DoesNotExist:
             return Response({"details":"there is no course found "},status = 400)

        if course.course_type != "PAID":
            return Response({"details":"this is a free course"},status=400)
        if course.status != "PUBLISHED":
            return Response({"details":"course is not published "},status=400)
        
        transaction =  Transactions.objects.create(
            tenant = user.tenant,
            user = user,
            course = course,
            amount = course.price,
            status = Transactions.PENDING
        )

        return Response({
          "payment_id":transaction.id,
          "status":transaction.status
        })
    
class Transaction_Verify(APIView):
    permission_classes = [IsAuthenticated]
    def post (self,request):
        verify = help_transaction()
        return verify.transaction(request)
    
class Transaction_Retry(APIView):
    permission_classes = [IsAuthenticated]
    def put(self,request):
       retry = help_transaction()
       return retry.transaction(request)

class Transaction_View(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user
        if user.role == UserRole.SUPER_ADMIN:
            data = Transactions.objects.all()
        elif user.role == UserRole.TENANT_ADMIN:
            data = Transactions.objects.filter(tenant = user.tenant)
        elif user.role == UserRole.TENANT_USER:
            data = Transactions.objects.filter(user = user)
        else:
            return Response({"details":"Not Authorized"},status=400)
    
        serializer = TransactionSerializers(data,many=True)
        return Response(serializer.data,status=200)
    
class help_transaction():
        def transaction(self, request):
            user = request.user
            if user.role != UserRole.TENANT_USER:
                return Response({"details":"tenent user can only pay"},status=403)
            payment = request.data.get("payment_id")
            success = request.data.get("success")

            if payment is None or success is None:
                return Response({"details":"payment id and success status is required"},status=403)
            try:
                transaction = Transactions.objects.get(
                    id = payment,
                    user = user,
                    tenant = user.tenant
                )
            except Transactions.DoesNotExist:
                return Response({"details":"no transaction data found"},status=403)
            
            if transaction.status ==Transactions.SUCCESS:
                return Response({"details":"Transaction is already complete"},status=200)
            
            if success:
                transaction.status =Transactions.SUCCESS
                transaction.payment_mode = "online"
                transaction.save()

                Enrollement.objects.get_or_create(
                    user = user,
                    course = transaction.course,
                    assigned_by = user,
                    defaults={
                        "status":Enrollement.ASSIGNED,
                        "self_enrolled":True
                    }
                )
                return Response({"details":"Payment is successful and the course is enrolled"},status=200)

            transaction.status = Transactions.FAILED
            transaction.save()
            return Response({"details":"Paymemt failed "},status=403)