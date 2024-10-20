import json
import uuid

import requests
import fal_client
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse, HttpRequest
from rest_framework.generics import ListAPIView
from rest_framework import authentication, permissions
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt

from services.api.requests import *
from .models import *
from payment.payment import PaymentAPI


class CheckFoodValueAPI(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest, food_name: str) -> JsonResponse:
        food_assitent = FoodAssistantRequestService()
        food_assitent_response = food_assitent.generate(food_name)
        return JsonResponse(food_assitent_response)


class ChatGPTAPI(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        data = request.data
        gpt_request = ChatGPTRequestService()
        response = gpt_request.generate(content=data['content'], temperature=data['temperature'])
        return JsonResponse(response)


class CheckProductAPI(ListAPIView):
    permission_classes = []

    def post(self, request: HttpRequest, *args, **kwargs) -> JsonResponse:
        data = request.data
        url_picture = data.get('url_picture')
        url = 'https://api.webastera.ru/api.php'
        data = {'action': 'yandex_picture', 'url_picture': url_picture}
        api_request = requests.post(url=url, json=data)
        api_response = api_request.json()
        return JsonResponse(api_response)


def index(request) -> HttpResponse:
    user_data = {'auth_user': request.user.is_authenticated}
    if request.user.is_authenticated:
        user_data['tariff'] = request.user.tariff
        user_data['balance'] = request.user.balance
    return render(request, "index.html", user_data)


def chatgpt(request) -> HttpResponse:
    user_data = {'auth_user': request.user.is_authenticated}
    if request.user.is_authenticated:
        user_data['tariff'] = request.user.tariff
        user_data['balance'] = request.user.balance
    return render(request, "chatgpt.html", user_data)


@csrf_exempt
def generate_assistant_request(request) -> JsonResponse:
    content = request.POST['content']
    assistant_request = AssistantRequestService()
    response = assistant_request.generate(content)
    return JsonResponse(response)


@csrf_exempt
def generate_chatgpt(request) -> JsonResponse:
    request = request.POST
    content = request['content']
    chat_gpt = ChatGPTService()
    response = chat_gpt.generate(content=content)
    return JsonResponse(response)


def fusion(request) -> HttpResponse:
    return render(request, 'fusion.html', {'auth_user': request.user.is_authenticated})


@csrf_exempt
def generate_fusion(request) -> JsonResponse:
    request = request.POST
    prompt = request['prompt']
    fusion = FusionService()
    uuid = fusion.generate(prompt=prompt)
    response = fusion.check_generation(uuid=uuid)
    return JsonResponse({'image': response})


def plusvector(request) -> HttpResponse:
    return render(request, 'plusvector.html')


@csrf_exempt
def generate_plusvector(request) -> JsonResponse:
    request = request.POST
    prompt = request['prompt']
    plus_vector = PlusVectorService(prompt=prompt)
    plus_vector_response = plus_vector.get()
    return JsonResponse({'images': plus_vector_response['response']['concepts']['images']})


def smartcamera(request) -> HttpResponse:
    user_data = {'auth_user': request.user.is_authenticated}
    if request.user.is_authenticated:
        user_data['tariff'] = request.user.tariff
        user_data['balance'] = request.user.balance
        return render(request, 'smartcamera.html', user_data)
    else:
        return render(request, 'unauthorized.html')


@csrf_exempt
def generate_smartcamera(request) -> JsonResponse:
    request_files = request.FILES
    image = request_files['file']  # Get image from request files.

    smart_camera = SmartCameraService()  # Init SmartCameraService instance.
    content = smart_camera.main(image_file=image.file)
    return JsonResponse({'asst_name': content['asst_name'], 'content': content['content'],
                        'yandex_data': content['yandex_data']})


def freesmartcamera(request):
    return render(request, 'freesmartcamera.html')


@csrf_exempt
def generate_freesmartcamera(request):
    request_files = request.FILES
    image = request_files['file']  # Get image from request files.

    free_smart_camera = FreeSmartCameraService()  # Init FreeSmartCameraService instance.
    response = free_smart_camera.main(image)
    return JsonResponse(response)


def chatgptplus(request) -> HttpResponse:
    return render(request, 'chatgptplus.html')


@csrf_exempt
def generate_chatgptplus(request) -> JsonResponse:
    request = request.POST
    content = request['content']
    chatgpt_plus = ChatGPTPlusService()
    response = chatgpt_plus.generate(content=content)
    return JsonResponse(response)


def flux(request) -> HttpResponse:
    user_data = {'auth_user': request.user.is_authenticated}
    if request.user.is_authenticated:
        user_data['tariff'] = request.user.tariff
        user_data['balance'] = request.user.balance
        return render(request, 'flux.html', user_data)
    else:
       return render(request, 'unauthorized.html')


@csrf_exempt
def generate_flux(request) -> JsonResponse:
    if request.user.is_authenticated:
        request = request.POST
        translator = TranslatorService()
        prompt = translator.translate(request['prompt'])

        def on_queue_update(update):
            if isinstance(update, fal_client.InProgress):
                for log in update.logs:
                    pass  # print(log["message"]))

        result = fal_client.subscribe(
            "fal-ai/flux-pro/v1.1",
            arguments={
                "prompt": prompt
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        return JsonResponse(result)
    else:
        return render(request, 'unauthorized.html')


@csrf_exempt
def signin(request) -> (HttpResponse | HttpResponseRedirect):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if not user:
                return JsonResponse({'status_code': 400, 'type': 'error', 'message': 'Неверная электронная почта!'})
            else:
                try:
                    user = authenticate(username=user.username, password=password)
                    if user is None:
                        return JsonResponse({'status_code': 400, 'type': 'error', 'message': 'Неверный пароль!'})
                    else:
                        login(request, user)
                        return JsonResponse({'status_code': 200, 'type': 'success', 'message': ''})
                except AttributeError:
                    return JsonResponse({'status_code': 400, 'type': 'error', 'message': 'Неверный пароль!'})
        except User.DoesNotExist:
            return JsonResponse({'status_code': 400, 'type': 'error', 'message': 'Такого пользователя не существует!'})
    return render(request, 'login.html')


@csrf_exempt
def signup(request) -> HttpResponseRedirect:
    email = request.POST['email']
    password = request.POST['password']
    retry_password = request.POST['retry_password']
    if password == retry_password:
        try:
            user = User.objects.get(email=email)
            if not user:
                return JsonResponse({'status_code': 200, 'type': 'select_tariff', 'message': ''})
            else:
                return JsonResponse({'status_code': 400, 'type': 'error', 'message': 'Такой пользователь уже существует!'})
        except User.DoesNotExist:
            return JsonResponse({'status_code': 200, 'type': 'select_tariff'})
    else:
        return JsonResponse({'status_code': 400, 'type': 'error', 'message': 'Пароли не совпадают!'})


@csrf_exempt
def logout_user(request) -> HttpResponseRedirect:
    logout(request)
    return JsonResponse({'status_code': 200, 'type': 'success', 'message': ''})


def tariff(request) -> HttpResponse:
    return render(request, 'tariff.html')


@csrf_exempt
def select_tariff(request) -> JsonResponse:
    request_data = request.POST
    tariff_id = request_data['tariff_id']
    tariff = Tariff.objects.get(tariff_id=tariff_id)
    payment_api = PaymentAPI()
    response = payment_api.get_payment_url(price=tariff.price, tariff_id=tariff_id)
    response = JsonResponse(response)
    return response


@csrf_exempt
def check_payment(request) -> JsonResponse:
    payment_id = request.POST['payment_id']
    payment_api = PaymentAPI()
    response = payment_api.check_payment(payment_id=payment_id)
    return JsonResponse(response)


@csrf_exempt
def create_user(request):
    tariff_id = request.POST['tariff_id']
    auth_temp_data = request.COOKIES.get('auth_temp_data')
    email, password, _ = list(json.loads(auth_temp_data).values())
    tariff = Tariff.objects.get(tariff_id=tariff_id)
    user = User.objects.create_user(username=str(uuid.uuid4()), email=email, password=password, tariff=tariff, balance=tariff.price)
    user = authenticate(username=user.username, password=password)
    login(request, user)
    response = JsonResponse({'status_code': 200, 'type': 'success', 'message': 'created'})
    response.delete_cookie('auth_temp_data')
    return response


def offer(request) -> HttpResponse:
    return render(request, 'offer.html')


def privacy_policy(request) -> HttpResponse:
    return render(request, 'privacy-policy.html')
