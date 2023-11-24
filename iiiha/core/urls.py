from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('chatgpt', chatgpt, name='chatgpt'),
    path('generate_chatgpt', generate_chatgpt, name='generate_chatgpt'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
