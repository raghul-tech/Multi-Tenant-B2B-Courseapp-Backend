from rest_framework import serializers
from skills.models import UserSkillProgress

class UserSkillProgress_View_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkillProgress
        fields = '__all__'
        read_only_fields = [field.name for field in model._meta.fields]

class UserSkillProgress_Create_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkillProgress
        fields = [
            "user",
            "tenant",
            "skills",
            "profeciency"
        ]
    
    def validate(self, attrs):
        user = self.context["request"].user
        if attrs['user'] != user:
            raise serializers.ValidationError("User not found")
        if attrs['tenant'] != user.tenant:
            raise serializers.ValidationError("Tenant not found")
        if attrs['skills'].tenant !=  user.tenant:
            raise serializers.ValidationError("Skill not found")
        
        if UserSkillProgress.objects.filter(
                user = attrs['user'],
                skills = attrs['skills']
            ).exists():
            raise serializers.ValidationError(" user skill is alreay there ")

        return super().validate(attrs)
    
    def create(self,validated_data):
        user = self.context['request'].user
        validated_data['tenant'] = user.tenant
        return super().create(validated_data)
