from rest_framework import serializers
from course.models import SubModule

class SubModuleSerializer(serializers.ModelSerializer):
    class Meta:
         model = SubModule
         fields =[
              "id",
              "title",
              "submodule_type",
              "orders",
              "video_url",
              "assignment_description",
              "module",
              "created_at",
              "updated_at",
         ]
         read_only_fields = ["id","created_at","updated_at"]

class SubModule_Details_Serializer(serializers.ModelSerializer):
     class Meta:
          model = SubModule
          fields = "__all__"