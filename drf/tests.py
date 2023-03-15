from rest_framework.test import APITestCase
from rest_framework import status
from drf.models import User, Lesson, Course


class LessonTestCase(APITestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User(email='aaa@mail.ru')
        self.user.set_password('1234')
        self.user.is_staff = False
        self.user.is_superuser = False
        self.user.save()

        response = self.client.post('/api/token/', {"email": "aaa@mail.ru", "password": "1234"})

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_course_create(self):
        response = self.client.post('/drf/course/',
                                    {
                                        "name": "asd",
                                        "preview": "test1",
                                        "description": "test1"
                                    }
                                    )
        print(f'test1: Started')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_create(self):
        self.test_course_create()
        response = self.client.post('/drf/lesson/create/',
                                    {
                                        "name": "test22",
                                        "description": "test1",
                                        "preview": "test1",
                                        "link": "https://www.youtube.com/watch?v=6zbgjwsCekI",
                                        "course_set": 1
                                    }
                                    )
        print(f'test2: Started')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_destroy(self):
        self.test_lesson_create()
        response = self.client.delete('/drf/lesson/destroy/1/')
        print(f'test3: Started')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_lesson_udate(self):
        self.test_lesson_create()
        response = self.client.patch('/drf/lesson/update/1/'
                                     , {
                                         "name": "lesson2218",
                                         "description": "test3",
                                         "preview": "test3",
                                         "link": "https://www.youtube.com/watch?v=6zbgjwsCekI",
                                         "course_set": 1
                                     }
                                     )
        print(f'test4: Started')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_getting_lessons_list(self):
        self.test_lesson_create()
        """
            Тестирование получения списка студентов
        """
        response = self.client.get(
            '/drf/lesson/'
        )
        self.lesson = Lesson.objects.get(pk=1)
        self.assertEqual(
            response.json(),
            [
                {
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": self.lesson.preview,
                    "link": self.lesson.link,
                    "course_set": self.lesson.course_set.pk,
                    "owner": self.lesson.owner.id,
                }
            ]
        )
        print(f'test5: Started')

    def test_subscribe(self):
        self.test_course_create()

        response = self.client.post('/drf/subscribed/',
                                    {
                                        "student": "aaa@mail.ru",
                                        "course": "asd"
                                    }
                                    )
        print(f'test6: Started')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscribe_status(self):
        self.test_subscribe()

        response = self.client.get('/drf/course/')
        self.course = Course.objects.get(pk=1)
        print(f'test7: Started')
        self.assertEqual(
            response.json(),
            [
                {
                    "name": self.course.name,
                    "description": self.course.description,
                    "preview": self.course.preview,
                    "all_lesson": 0,
                    "lessons": [],
                    "owner": self.course.owner.id,
                    "subscription": "Subscribed"
                }
            ]
        )
