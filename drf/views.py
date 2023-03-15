from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status, serializers
from rest_framework.response import Response
from drf.models import Course, Lesson, Subscribe, User
from drf.permissions import OwnerPerms, ModerPerms, OwnerSubscribePerm
from drf.serlizers import CourseSerializer, LessonSerializer, SubscribeSerializer, PaymentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [ModerPerms | OwnerPerms]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            raise f'Модератор не может создавать уроки'
        else:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['owner'] = request.user.pk
            request.data._mutable = _mutable
            answer = super().create(request, *args, **kwargs)
        return answer

    def retrieve(self, request, pk=None):
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        if self.request.user.is_staff:
            raise serializers.ValidationError('Модератор не может удалять курсы')
        else:
            request.data['owner'] = request.user.pk
            answer = super().create(request, *args, **kwargs)
        return answer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonListView(generics.ListAPIView):
    permission_classes = [ModerPerms | OwnerPerms]
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    permission_classes = [OwnerPerms]
    serializer_class = LessonSerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            raise f'Модератор не может создавать курсы'
        else:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['owner'] = request.user.pk
            request.data._mutable = _mutable
            answer = super().create(request, *args, **kwargs)
        return answer


class LessonDeleteAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            raise f'Модератор не может удалять уроки'
        return queryset.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(owner=self.request.user)


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            raise serializers.ValidationError('Модератор не может создавать оплаты')
        else:
            request.data['user'] = request.user.pk
            answer = super().create(request, *args, **kwargs)
            Subscribe.objects.create(subscribe_status=True)
            print(Subscribe.course)

        return answer


class SubscribeListAPIView(generics.ListAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()


class SubscribeCreateAPIView(generics.CreateAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()

    def post(self, request, *args, **kwargs):
        """Проверка данных на уникальность и создание экземпляра если данные уникальны"""
        data_student = User.objects.filter(email=request.data['student']).first()
        data_course = Course.objects.filter(name=request.data['course']).first()
        obj = self.queryset.filter(student=data_student).filter(course=data_course)
        if not obj:
            return self.create(request, *args, **kwargs)
        return Response(request.data, status=status.HTTP_200_OK)


class SubscribeDestroyAPIView(generics.DestroyAPIView):
    serializer_class = SubscribeSerializer
    queryset = Subscribe.objects.all()
    permission_classes = [OwnerSubscribePerm]
