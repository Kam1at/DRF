from rest_framework import viewsets, generics
from drf.models import Course, Lesson
from drf.permissions import OwnerPerms, ModerPerms
from drf.serlizers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [ModerPerms | OwnerPerms]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def create(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            raise f'Модератор не может создавать уроки'
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
            request.data['owner'] = request.user.pk
            answer = super().create(request, *args, **kwargs)
        return answer

    def destroy(self, request, *args, **kwargs):

        if self.request.user.is_staff:
            raise f'Модератор не может удалять курсы'
        else:
            request.data['owner'] = request.user.pk
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
