from rest_framework import serializers
from .models import Department, Course, Section, SectionDetails, SectionDays, SectionChain, SectionChainDays

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class SectionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionDetails
        fields = '__all__'

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class SectionDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionDays
        fields = '__all__'

class SectionChainSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionChain
        fields = '__all__'

class SectionChainDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionChainDays
        fields = '__all__'
