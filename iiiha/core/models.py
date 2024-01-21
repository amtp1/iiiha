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
