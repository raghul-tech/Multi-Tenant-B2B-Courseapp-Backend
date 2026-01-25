from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from course.models import Course_db
from core.permission import UserRole
from enrollement.models import Enrollement
from .models import Transactions
from .serializers import TransactionSerializers
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


stripe.api_key = settings.STRIPE_SECRET_KEY
WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET

# Create your views here.
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
        if Transactions.objects.filter(
               user = user,
            course = course,
            status = Transactions.SUCCESS
        ).exists():
            return Response({"Course is already paid"},status=200)
        elif Transactions.objects.filter(
              user = user,
            course = course,
            status = Transactions.PENDING
        ).exists():
            return Response({"Transaction is in pending cant pay again"},status=200)
        
        transaction =  Transactions.objects.create(
            tenant = user.tenant,
            user = user,
            course = course,
            amount = course.price,
            status = Transactions.PENDING
        )

        payment_intent = stripe.PaymentIntent.create(
            amount=int(course.price * 100),  # convert to paise
            currency="inr",
        automatic_payment_methods={
        "enabled": True,
        "allow_redirects": "never"
    },
            metadata={
                "transaction_id": transaction.id,
                "user_id": user.id,
                "tenant_id": user.tenant.id,
                "course_id": course.id,
            }
        )
        transaction.stripe_payment_id = payment_intent.id
        transaction.save()

        return Response({
          "payment_id":transaction.id,
          "status":transaction.status,
          "client_secret": payment_intent.client_secret,
          "stripe_payment_id":transaction.stripe_payment_id
        },status=201)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebHook(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        payload = request.body
        signature = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError:
            return Response(status=400)
        except ValueError as e:
             return Response({"error": str(e)}, status=400)

        
        if event['type'] == 'payment_intent.succeeded':
            self.success(event['data']['object'])
        elif event['type'] == 'payment_intent.payment_failed':
            self.failed(event['data']['object'])
            
        return Response(status=200)

    def success(self,event):
        transaction_id = event['metadata'].get('transaction_id')

        try:
           transaction =   Transactions.objects.get(id = transaction_id)
        except Transactions.DoesNotExist:
            return
        if transaction.status == Transactions.SUCCESS:
            return
        
        transaction.status = Transactions.SUCCESS
        transaction.stripe_payment_id = event['id']
        transaction.payment_mode = 'stripe'
        transaction.save()
        Enrollement.objects.get_or_create(
                    user = transaction.user,
                    course = transaction.course,
                    assigned_by = transaction.user,
                    defaults={
                        "status":Enrollement.ASSIGNED,
                        "self_enrolled":True
                    }
                )
        
    def failed(self,event):
        transaction_id = event['metadata'].get('transaction_id')
        try:
           transaction =   Transactions.objects.get(id = transaction_id)
           transaction.status = Transactions.FAILED
           transaction.save()
        except Transactions.DoesNotExist:
            return
        