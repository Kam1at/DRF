from rest_framework import serializers
from drf.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = (
            'id',
            'name',
            'description',
            'preview',
            'link',
            'course_set',
            'owner'
        )


class CourseSerializer(serializers.ModelSerializer):
    all_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set')

    class Meta:
        model = Course
        fields = (
            'name',
            'preview',
            'description',
            'all_lesson',
            'lessons',
            'owner'
        )

        def get_all_lesson(self, instance):
            all_less = Lesson.objects.filter(course_set=instance)
            if all_less:
                return len(all_less)
            else:
                return 0
