from rest_framework import serializers
from  .models import Course_db
from .module.serializers import Module_Details_Serializer
from skills.models import Skills,CourseSkill


class CourseSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.SerializerMethodField()

    class Meta:
        model = CourseSkill
        fields = ["skill_name", "course_weight"]

    def get_skill_name(self, obj):
        return obj.skills.name

class CourseSerializer(serializers.ModelSerializer):
    skills=  CourseSkillSerializer(
        source = "courseskill_set",
        many=True,read_only=True)
    class Meta: 
        model = Course_db
        fields = [
            'id',
            'title',
            'description',
            'image',
            'created_at',
            'updated_at',
            'course_type',
            'price',
            'status',
            "skills"
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class AddSkillSerializer(serializers.Serializer):
    name = serializers.CharField()
    weight = serializers.IntegerField(min_value=1,max_value=100)

class CourseCreateSerializer(serializers.ModelSerializer):
    skills = AddSkillSerializer(many= True,write_only = True)
    class Meta:
        model = Course_db
        fields =[
            "id",
            'title',
            'tenant',
            'created_by',
            'description',
            'image',
             'course_type',
             'price',
            'status',
            'skills'
        ]
    
    def validate_skills(self, skills):
     if not skills or len(skills) == 0:
        raise serializers.ValidationError(
            "At least one skill is required for a course."
        )
     return skills


    def validate(self, attrs):
        title = attrs.get('title')
        tenant = self.context['request'].user.tenant
        if Course_db.objects.filter(title = title,tenant = tenant).exists():
            raise serializers.ValidationError("Course already Exists")
        price = attrs.get("price")
        status = attrs.get("status")
        if status == Course_db.FREE and price != 0:
            raise serializers.ValidationError(
                "Free course must have price 0"
            )
        if status == Course_db.PAID and price <= 0:
            raise serializers.ValidationError(
                "Paid course must have price greater than 0"
            )     
        
        skills = attrs.get("skills", [])
        total_weight = sum(skill["weight"] for skill in skills)

        if total_weight > 100:
            raise serializers.ValidationError(
                "Total skill weight cannot exceed 100"
            )

        return attrs

    def create(self, validated_data):
        skills = validated_data.pop('skills')
        user = self.context['request'].user
        tenant = user.tenant
        course = Course_db.objects.create(
            tenant = tenant,
            created_by = user,
            **validated_data)

        for skill_name in skills:
            skill,_ = Skills.objects.get_or_create(
                name = skill_name['name'],
                 tenant = tenant
            )
            CourseSkill.objects.get_or_create(
                tenant= tenant,
                course = course,
                skills = skill,
                course_weight = skill_name['weight']
            )


        return course
    
class CourseEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_db
        fields = [
            "title",
            "description",
            "image",
            "status",
            "price",
            "course_type"
        ]
    def validate(self, attrs):
        price = attrs.get("price", self.instance.price)
        status = attrs.get("status", self.instance.status)
        if status == Course_db.FREE and price != 0:
            raise serializers.ValidationError(
                "Free course must have price 0"
            )

        if status == Course_db.PAID and price <= 0:
            raise serializers.ValidationError(
                "Paid course must have price greater than 0"
            )

        return super().validate(attrs)


class Course_Details_Serializer(serializers.ModelSerializer):
     class Meta: 
        model = Course_db
        fields = "__all__"

     modules = Module_Details_Serializer(many=True,read_only=True)

