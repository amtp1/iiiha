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
    path('generate_fusion', generate_fusion, name='generate_fusion'),
    path('plusvector', plusvector, name='plusvector'),
    path('generate_plusvector', generate_plusvector, name='generate_plusvector'),
    path('smartcamera', smartcamera, name='smartcamera'),
    path('generate_smartcamera', generate_smartcamera, name='generate_smartcamera'),

    # API urls
    path('api/checkfoodvalue/<str:food_name>', CheckFoodValueAPI.as_view(), name="checkfoodvalue")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
