import json
import uuid

import requests
import fal_client
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse, HttpRequest
from rest_framework.generics import ListAPIView
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt

from services.api.requests import *
from .models import *


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
    return render(request, "index.html", {'auth_user': request.user.is_authenticated})


def chatgpt(request) -> HttpResponse:
    return render(request, "chatgpt.html", {'auth_user': request.user.is_authenticated})


@csrf_exempt
def generate_assistant_request(request):
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
    if request.user.is_authenticated:
        return render(request, 'smartcamera.html', {'auth_user': request.user.is_authenticated})
    else:
        return JsonResponse({'error': 'Unauthorized!'})


@csrf_exempt
def generate_smartcamera(request) -> JsonResponse:
    request_files = request.FILES
    image = request_files['file']  # Get image from request files.

    # ===> Hide image save function for time.
    # image_obj = SmartCamera.objects.create(image=image)
    # image_url = f"http://{request.get_host()}{image_obj.image.url}"

    smart_camera = SmartCameraService()  # Init SmartCameraService instance.
    content = smart_camera.main(image_file=image.file)
    return JsonResponse({'asst_name': content['asst_name'], 'content': content['content'],
                        'yandex_data': content['yandex_data']})


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
    return render(request, 'flux.html', {'auth_user': request.user.is_authenticated})


@csrf_exempt
def generate_flux(request) -> JsonResponse:
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


def signin(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.get(email=email)
            if not user:
                return render(request, 'login.html', {'message': 'Неверная электронная почта!'})
            else:
                try:
                    user = authenticate(username=user.username, password=password)
                    login(request, user)
                    return redirect('index')
                except AttributeError:
                    return render(request, 'login.html', {'message': 'Неверный пароль!'})
        except User.DoesNotExist:
            return render(request, 'login.html', {'message': 'Такого пользователя не существует!'})
    return render(request, 'login.html')


def signup(request):
    email = request.POST['email']
    password = request.POST['password']
    retry_password = request.POST['retry_password']
    username = uuid.uuid1()
    if password == retry_password:
        try:
            user = User.objects.get(email=email)
            if not user:
                response = redirect('tariff')
                response.set_cookie('auth_temp_data', json.dumps({'email': email, 'password': password,
                                                       'username': str(username)}))
                return response
                # return redirect('tariff')
                # user = User.objects.create_user(username=username, email=email, password=password)
                # user = authenticate(username=username, password=password)
                # return redirect('index')
            else:
                return render(request, 'login.html', {'message': 'Такой пользователь уже существует!'})
        except User.DoesNotExist:
            response = redirect('tariff')
            response.set_cookie('auth_temp_data', json.dumps({'email': email, 'password': password,
                                                   'username': str(username)}))
            return response
            # return redirect('tariff')
            #user = User.objects.create_user(username=username, email=email, password=password)
            #user = authenticate(username=username, password=password)
            #login(request, user)
            #return redirect('index')


def logout_user(request):
    logout(request)
    return redirect('index')


def tariff(request):
    return render(request, 'tariff.html')


def select_tariff(request):
    request_data = request.POST
    tariff_id = request_data['tariff_id']
    auth_temp_data = request.COOKIES.get('auth_temp_data')
    email, password, username = list(json.loads(auth_temp_data).values())
    user = User.objects.create_user(username=username, email=email, password=password)
    tariff = Tariff.objects.get(tariff_id=tariff_id)
    TariffSet.objects.create(user=user, tariff=tariff)
    user = authenticate(username=username, password=password)
    login(request, user)
    return JsonResponse({'response': True})


def offer(request):
    return render(request, 'offer.html')


def privacy_policy(request):
    return render(request, 'privacy-policy.html')
