from rest_framework import serializers
from .models import Catalogues
from .catalogues_course.serializers import Catalogues_Details_Serializers

class Catalogues_Serializers(serializers.ModelSerializer):
   class Meta:
      model = Catalogues
      fields =  [
         "id",
         "name",
         "is_active",
         "created_by",
         "tenant",
         "created_at",
         "updated_at"
      ]
      read_only_fields =["id","created_at","updated_at","tenant","created_by"]



class Catalogues_Details_Serializers(serializers.ModelSerializer):
   class Meta:
      model = Catalogues
      fields = "__all__"
   
   catalogue_id= Catalogues_Details_Serializers(many=True,read_only=True)