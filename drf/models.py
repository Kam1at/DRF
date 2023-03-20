from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name='почта',
        unique=True
    )

    number = models.CharField(max_length=25, verbose_name='номер телефона')
    avatar = models.ImageField(verbose_name='аватар', upload_to='users/')
    city = models.CharField(max_length=35, verbose_name='страна')
    token = models.CharField(max_length=250, verbose_name='токен')
    token_created = models.DateTimeField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email} {self.number} {self.avatar}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    preview = models.CharField(max_length=200, verbose_name='Превью', **NULLABLE)
    description = models.CharField(max_length=250, verbose_name='Описание')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.IntegerField(default=15000)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.CharField(max_length=250, verbose_name='Описание')
    preview = models.CharField(max_length=200, verbose_name='Превью', **NULLABLE)
    link = models.URLField(max_length=200, verbose_name='Ссылка на видео')
    course_set = models.ForeignKey(Course, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} {self.description} {self.preview} {self.link}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payment(models.Model):
    PAYMENT_CARD = 'card'
    PAYMENT_CASH = 'cash'
    PAYMENTS = (
        (PAYMENT_CARD, 'карта'),
        (PAYMENT_CASH, 'наличные')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_date = models.DateField(verbose_name='дата оплаты', null=True)
    payment_course = models.CharField(max_length=250, verbose_name='название оплаченного курса')
    payment_sum = models.PositiveIntegerField(verbose_name='сумма оплаты')
    payment_type = models.CharField(choices=PAYMENTS, default=PAYMENT_CARD, max_length=10, verbose_name='тип оплаты')

    def __str__(self):
        return f'{self.user},{self.payment_course},{self.payment_sum},'


class PaymentLog(models.Model):
    Success = models.BooleanField(verbose_name='успешность платежа')
    ErrorCode = models.CharField(max_length=250, verbose_name='код ошибки')
    TerminalKey = models.CharField(max_length=250, verbose_name='ключ терминала')
    Status = models.CharField(max_length=250, verbose_name='статус платежа')
    PaymentId = models.CharField(max_length=250, verbose_name='айди платежа')
    OrderId = models.CharField(max_length=250, verbose_name='айди заявки')
    Amount = models.IntegerField(verbose_name='сумма оплаты')
    PaymentURL = models.URLField(verbose_name='ссылка на оплату')
    PaymentDate = models.DateField(auto_now_add=True, verbose_name='дата создания')


class Subscribe(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='студент')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс')
