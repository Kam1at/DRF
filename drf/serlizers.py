from rest_framework import serializers
from drf.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            'name',
            'preview',
            'description'
        )


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = (
            'name',
            'description',
            'preview',
            'link'
        )
