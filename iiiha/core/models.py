from os.path import splitext
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User


class UUIDFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/{uuid4().hex + ext}"


class SmartCamera(models.Model):
    image = models.ImageField(storage=UUIDFileStorage())


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

    def __str__(self):
        return f"Тариф #{self.tariff_id} - {self.name}"

    class Meta:
        db_table = "tariffs"
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"


class TariffSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE)

    def __str__(self):
        return f"Соотношение #{self.user} - {self.tariff}"

    class Meta:
        db_table = "tariff_sets"
        verbose_name = "Соотношение пользователя к тарифу"
        verbose_name_plural = "Соотношения пользователя к тарифу"
