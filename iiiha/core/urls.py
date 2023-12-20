from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('generate_assistent_request', generate_assistent_request, name='generate_assistent_request'),
    path('chatgpt', chatgpt, name='chatgpt'),
    path('generate_chatgpt', generate_chatgpt, name='generate_chatgpt'),
    path('fusion', fusion, name='fusion'),
    path('generate_fusion', generate_fusion, name='generate_fusion')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
