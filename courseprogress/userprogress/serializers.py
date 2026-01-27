from rest_framework import serializers
from courseprogress.models import UserProgress

class UserProgressSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]


class UserProgressEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = ["last_watched_duration", "mark_scored"]

    def validate(self, attrs):
        progress = self.instance.submodule_progress
        submodule = progress.submodule

        if submodule.submodule_type == "VIDEO":
            if "last_watched_duration" not in attrs:
                raise serializers.ValidationError(
                    {"last_watched_duration": "Required for video"}
                )
            if attrs["last_watched_duration"] > submodule.video_duration:
                raise serializers.ValidationError(
                    {"last_watched_duration": "Cannot exceed video duration"}
                )
            
        if submodule.submodule_type == "ASSIGNMENT":
            if "mark_scored" not in attrs:
                raise serializers.ValidationError(
                    {"mark_scored": "Required for assignment"}
                )
            if attrs["mark_scored"] > submodule.assignment_mark:
                raise serializers.ValidationError(
                    {"mark_scored": "Cannot exceed assignment marks"}
                )

        return attrs


