from rest_framework import serializers
from course.models import SubModule,Module

class SubModuleSerializer(serializers.ModelSerializer):
    class Meta:
         model = SubModule
         fields = "__all__"
         read_only_fields = [field.name for field in model._meta.fields]


class SubModule_Details_Serializer(serializers.ModelSerializer):
     class Meta:
          model = SubModule
          fields = "__all__"

class SubModuleCreateSerializer(serializers.ModelSerializer):
     class Meta:
          model = SubModule
          fields = [
               "module",
              "title",
              "submodule_type",
              "order",
              "url",
              "description",   
              "video_duration",
              "assignment_mark",
          ]

     def validate(self, attrs):
          return validate_submodule(self,attrs)
     
class SubModuleEditSerializer(serializers.ModelSerializer):
     class Meta:
          model = SubModule
          fields=[
              "title",
              "submodule_type",
              "order",
              "url",
              "description",   
              "video_duration",
              "assignment_mark",
          ]
     def validate(self, attrs):
          return validate_submodule(self,attrs)
     
def validate_submodule(self, attrs):
    instance = self.instance

    submodule_type = attrs.get(
        "submodule_type",
        getattr(instance, "submodule_type", None)
    )

    video_duration = attrs.get(
        "video_duration",
        getattr(instance, "video_duration", None)
    )

    assignment_mark = attrs.get(
        "assignment_mark",
        getattr(instance, "assignment_mark", None)
    )

    url = attrs.get(
        "url",
        getattr(instance, "url", None)
    )

    order = attrs.get("order", getattr(instance, "order", None))
    module = attrs.get("module", getattr(instance, "module", None))

    if order and order > 1:
        if not SubModule.objects.filter(module=module, order=order - 1).exists():
            raise serializers.ValidationError(
                "Previous submodule must exist before adding this order."
            )
        
    if submodule_type == "VIDEO":
        if not video_duration:
            raise serializers.ValidationError(
                {"video_duration": "Video duration is required for video submodules."}
            )
        if assignment_mark:
            raise serializers.ValidationError(
                {"assignment_mark": "Assignment mark is not allowed for video submodules."}
            )

    elif submodule_type == "ASSIGNMENT":
        if not assignment_mark:
            raise serializers.ValidationError(
                {"assignment_mark": "Assignment mark is required for assignment submodules."}
            )
        if video_duration:
            raise serializers.ValidationError(
                {"video_duration": "Video duration is not allowed for assignment submodules."}
            )

    else:
        raise serializers.ValidationError(
            {"submodule_type": "Invalid submodule type."}
        )
    
    if not url:
            raise serializers.ValidationError(
                {"url": "Video URL is required for submodules."}
            )

    return attrs



