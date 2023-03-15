from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from drf.models import Course, Lesson, Subscribe, User, Payment
from drf.validators import YouTubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        validators = [YouTubeLinkValidator(field='link')]
        fields = (
            'name',
            'description',
            'preview',
            'link',
            'course_set',
            'owner'
        )


class SubscribeSerializer(serializers.ModelSerializer):
    student = SlugRelatedField(slug_field="email", queryset=User.objects.all())
    course = SlugRelatedField(slug_field="name", queryset=Course.objects.all())

    class Meta:
        model = Subscribe
        fields = ('student', 'course')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = (
            'user',
            'payment_date',
            'payment_course',
            'payment_sum',
            'payment_type'
        )


class CourseSerializer(serializers.ModelSerializer):
    all_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, source='lesson_set', required=False)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = (
            'name',
            'preview',
            'description',
            'all_lesson',
            'lessons',
            'subscription',
            'owner',
        )

    def get_all_lesson(self, instance):
        all_less = Lesson.objects.filter(course_set=instance)
        if all_less:
            return len(all_less)
        else:
            return 0

    def get_subscription(self, course):
        user = self.context['request'].user.id

        obj = Subscribe.objects.filter(course=course.id).filter(student=user)
        if obj:
            return 'Subscribed'
        return 'Unsubscribed'
