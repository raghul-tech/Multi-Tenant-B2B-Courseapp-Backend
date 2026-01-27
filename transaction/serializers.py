from rest_framework import serializers
from .models import Transactions


class TransactionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'