from rest_framework import serializers
from .models import Tenant
from rest_framework.response import Response


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ['id', 'name', 'is_active', 'created_at']

  #  def create(self, validated_data):
   #     tenant = Tenant(**validated_data)
   #     tenant.save()
   #     return tenant