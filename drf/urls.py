from django.urls import path
from rest_framework.routers import DefaultRouter
from drf.views import CourseViewSet, LessonListView, LessonDeleteAPIView, LessonUpdateAPIView, LessonCreateAPIView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/', LessonListView.as_view(), name='lesson_list'),
                  path('lesson/create', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lesson/destroy/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_destroy'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
              ] + router.urls
