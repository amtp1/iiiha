from enum import Enum
from os.path import splitext
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User


class UUIDFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/{uuid4().hex + ext}"


class SmartCamera(models.Model):
    image = models.ImageField(storage=UUIDFileStorage(), verbose_name='Изображение')


class Assistant(models.Model):
    key_word = models.CharField(max_length=255, verbose_name='Ключевое слово')
    asst_id = models.CharField(max_length=255, verbose_name='Id ассистента')

    def __str__(self):
        return f"Ассистент #{self.id}, ID: {self.asst_id}"

    class Meta:
        db_table = "assistants"
        verbose_name = "Ассистент"
        verbose_name_plural = "Ассистенты"


class Tariff(models.Model):
    tariff_id = models.IntegerField(verbose_name='Идентификатор тарифа')
    name = models.CharField(max_length=255, verbose_name='Название тарифа')
    price = models.IntegerField(default=0, null=False, verbose_name='Цена тарифа')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "tariffs"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class User(AbstractUser):
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, verbose_name='Тариф')
    balance = models.FloatField(default=0.0, null=False, verbose_name='Баланс')

    class Meta:
        db_table = "auth_user"


class Payment(models.Model):
    class Status(Enum):
        success = ("success", "Успешно")
        in_progress = ("in_progress", "В процессе")

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    payment_id = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=32,
        choices=[x.value for x in Status],
        default=Status.get_value("in_progress"),
        verbose_name="Статус оплаты",
    )
    created = models.DateTimeField(verbose_name="Дата платежа", default=timezone.now)
    updated = models.DateTimeField(
        verbose_name="Дата обновления",
        auto_now=True,
        auto_now_add=False,
        blank=True,
        null=True
    )

    class Meta:
        db_table = "payments"
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"


class Service(models.Model):
    class ServiceName(Enum):
        smartcamera = ("smartcamera", "Smart Camera")
        flux = ("flux", "Flux")
        kling = ("kling", "Kling")

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    name = models.CharField(
        unique=True,
        max_length=32,
        choices=[x.value for x in ServiceName],
        default=ServiceName.get_value("smartcamera"),
        verbose_name="Имя сервиса",
    )
    price = models.FloatField(default=0.0, verbose_name='Цена за 1 генерацию')

    class Meta:
        db_table = "services"
        verbose_name = "Сервис"
        verbose_name_plural = "Сервисы"
