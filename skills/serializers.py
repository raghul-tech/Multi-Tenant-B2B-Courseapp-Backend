from rest_framework import serializers
from .models import Skills


class Skills_View_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = [
            "id",
            "tenant",
            "name",
            "is_active",
            "created_at"
        ]
        read_only_fields = [field.name for field in model._meta.fields]

class Skills_Edit_Serializers(serializers.ModelSerializer):
     class Meta:
          model = Skills
          fields = [
               "name",
               "is_active"
          ]
      

class Skills_Create_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields =[
             "name",
            "is_active",
        ]
    def validate_name(self,value):
            user = self.context["request"].user
            if Skills.objects.filter(
                name = value,
                tenant = user.tenant
            ).exists():
                raise serializers.ValidationError(
                    "the skill is already in the database"
                )
            return value
        
    def create(self,validated_data):
            user = self.context["request"].user
            validated_data['tenant'] = user.tenant
            return super().create(validated_data)


      
            
            

