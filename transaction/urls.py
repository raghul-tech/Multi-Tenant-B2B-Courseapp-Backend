from django.urls import path
from .views import Transaction_Initialize,Transaction_Verify,Transaction_View,Transaction_Retry


urlpatterns =[
    path('initialize/',Transaction_Initialize.as_view(),name = "transaction-intialize"),
    path('verify/',Transaction_Verify.as_view(),name = "transaction-verify"),
    path('verify/retry/',Transaction_Retry.as_view(),name = "transaction-retry"),
    path('view/',Transaction_View.as_view(),name = "transaction-view"),
]