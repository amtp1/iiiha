from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('generate_assistant_request', generate_assistant_request, name='generate_assistant_request'),
    path('chatgpt', chatgpt, name='chatgpt'),
    path('generate_chatgpt', generate_chatgpt, name='generate_chatgpt'),
    path('fusion', fusion, name='fusion'),
    path('generate_fusion', generate_fusion, name='generate_fusion'),
    path('plusvector', plusvector, name='plusvector'),
    path('generate_plusvector', generate_plusvector, name='generate_plusvector'),
    path('smartcamera', smartcamera, name='smartcamera'),
    path('generate_smartcamera', generate_smartcamera, name='generate_smartcamera'),
    path('chatgptplus', chatgptplus, name='chatgptplus'),
    path('generate_chatgptplus', generate_chatgptplus, name='generate_chatgptplus'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('logout', logout_user, name='logout_user'),

    # API urls
    path('api/checkfoodvalue/<str:food_name>', CheckFoodValueAPI.as_view(), name="checkfoodvalue"),
    path('api/chatgpt', ChatGPTAPI.as_view(), name="chatgpt"),
    path('api/check_product', CheckProductAPI.as_view(), name="check_product")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.TEMP_URL, document_root=settings.TEMP_ROOT)
