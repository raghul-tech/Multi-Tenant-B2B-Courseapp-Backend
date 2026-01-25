from rest_framework import serializers
from .models import Transactions


class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = [
            "id",
            "user",
            "tenant",
            "course",
            "payment_mode",
            "amount",
            "status"
        ]