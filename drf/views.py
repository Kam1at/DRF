import datetime

from django.contrib.sites import requests
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from drf.models import Course, Lesson, Subscribe, User, Payment, PaymentLog
from drf.permissions import OwnerPerms, ModerPerms, OwnerSubscribePerm
from drf.serlizers import CourseSerializer, LessonSerializer, SubscribeSerializer, PaymentSerializer, \
    PaymnetlogSerializer


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


class PaymentAPIView(APIView):
    def get(self, *args, **kwargs):
        course_pk = self.kwargs.get('pk')
        course_item = get_object_or_404(Course, pk=course_pk)

        order_id = Payment.objects.create(
            payment_course=course_item,
            payment_sum=course_item.price,
            user=self.request.user,
            payment_date=datetime.datetime.now().date(),
            payment_type=Payment.PAYMENT_CARD
        )

        data_for_request = {
            "TerminalKey": settings.TERMINAL_KEY,
            "Amount": course_item.price,
            "OrderId": order_id.pk,
            "Receipt": {
                "Email": "a@test.ru",
                "Phone": "+79031234567",
                "EmailCompany": "b@test.ru",
                "Taxation": "osn",
                "Items": [
                    {
                        "Name": course_item.course_title,
                        "Price": course_item.price,
                        "Quantity": 1.00,
                        "Amount": course_item.price,
                        "PaymentMethod": "full_prepayment",
                        "PaymentObject": "commodity",
                        "Tax": "vat10",
                        "Ean13": "0123456789"
                    }
                ]
            }
        }

        response = requests.post('https://securepay.tinkoff.ru/v2/Init/', json=data_for_request)

        PaymentLog.objects.create(
            Success=response.json()['Success'],
            ErrorCode=response.json()['ErrorCode'],
            TerminalKey=response.json()['TerminalKey'],
            Status=response.json()['Status'],
            PaymentId=response.json()['PaymentId'],
            OrderId=response.json()['OrderId'],
            Amount=response.json()['Amount'],
            PaymentURL=response.json()['PaymentURL']
        )

        if response.json()['Success']:
            Subscribe.objects.create(
                student=self.request.user,
                course=course_item
            )

        print(response.json())
        return Response(
            {
                'url': response.json()['PaymentURL']
            }
        )


class PaymentlogList(generics.ListAPIView):
    serializer_class = PaymnetlogSerializer
    queryset = PaymentLog.objects.all()


class PaymentList(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
