from rest_framework import serializers
from catalogues.models import Catalogues_Courses

class Catalogues_Course_Serializers(serializers.ModelSerializer):
   class Meta:
      model = Catalogues_Courses
      fields = [
         "id",
         "order",
         "catalogue",
         "course"
      ]
      read_only_fields=["id","catalogue"]

class Catalogues_Details_Serializers(serializers.ModelSerializer):
   class Meta:
      model = Catalogues_Courses
      fields = "__all__"

