from rest_framework import serializers
from courseprogress.models import UserSubModuleProgress

class submoduleProgress_view_serializers(serializers.ModelSerializer):
    class Meta:
        model = UserSubModuleProgress
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]

