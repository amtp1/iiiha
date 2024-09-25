from os.path import splitext
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class UUIDFileStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None) -> str:
        _, ext = splitext(name)
        return F"{settings.MEDIA_ROOT}/{uuid4().hex + ext}"


class SmartCamera(models.Model):
    image = models.ImageField(storage=UUIDFileStorage())


class Assistants(models.Model):
    key_word = models.CharField(max_length=255, verbose_name='Ключевое слово')
    asst_id = models.CharField(max_length=255, verbose_name='Id ассистента')

    def __str__(self):
        return f"Ассистент №{self.id}, ID: {self.asst_id}"

    class Meta:
        db_table = "assistants"
        verbose_name = "Ассистент"
        verbose_name_plural = "Ассистенты"
