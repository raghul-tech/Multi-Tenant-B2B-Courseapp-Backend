from django.urls import path
from .views import Transaction_Initialize,Transaction_View,StripeWebHook


urlpatterns =[
    path('start/',Transaction_Initialize.as_view(),name = "transaction-intialize"),
    path('view/',Transaction_View.as_view(),name = "transaction-view"),
    path("stripe/webhook/",StripeWebHook.as_view(),name="stripe-webhook")
]