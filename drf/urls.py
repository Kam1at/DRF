from django.urls import path
from rest_framework.routers import DefaultRouter
from drf.views import CourseViewSet, LessonListView, LessonDeleteAPIView, LessonUpdateAPIView, LessonCreateAPIView, \
    SubscribeCreateAPIView, SubscribeDestroyAPIView, SubscribeListAPIView, PaymentCreateAPIView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
                  path('lesson/', LessonListView.as_view(), name='lesson_list'),
                  path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
                  path('lesson/destroy/<int:pk>/', LessonDeleteAPIView.as_view(), name='lesson_destroy'),
                  path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
                  path('create/', PaymentCreateAPIView.as_view(), name='payment_create'),
                  path('list/', SubscribeListAPIView.as_view(), name='subscribe_list'),
                  path('subscribed/', SubscribeCreateAPIView.as_view(), name='subscribed'),
                  path('unsubscribed/<int:pk>/', SubscribeDestroyAPIView.as_view(), name='unsubscribed'),
              ] + router.urls
