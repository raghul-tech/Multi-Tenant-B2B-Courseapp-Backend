from rest_framework import serializers
from courseprogress.models import UserModuleProgress

class moduleProgress_view_serializers(serializers.ModelSerializer):
    class Meta:
        model = UserModuleProgress
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]
    

        

        
