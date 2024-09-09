from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, HttpRequest
from rest_framework.generics import ListAPIView
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view

from django.views.decorators.csrf import csrf_exempt

from services.api.requests import *
from .models import *


class CheckFoodValueAPI(ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: HttpRequest, food_name: str) -> JsonResponse:
        food_assitent = FoodAssistentRequestService()
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


def index(request) -> HttpResponse:
    return render(request, "index.html")


def chatgpt(request) -> HttpResponse:
    return render(request, "chatgpt.html")


@csrf_exempt
def generate_assistent_request(request):
    content = request.POST['content']
    assistent_request = AssistentRequestService()
    response = assistent_request.generate(content)
    return JsonResponse(response)


@csrf_exempt
def generate_chatgpt(request) -> JsonResponse:
    request = request.POST
    content = request['content']
    chat_gpt = ChatGPTService()
    response = chat_gpt.generate(content=content)
    return JsonResponse(response)


def fusion(request) -> HttpResponse:
    return render(request, 'fusion.html')


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
    return render(request, 'smartcamera.html')


@csrf_exempt
def generate_smartcamera(request) -> JsonResponse:
    request_files = request.FILES
    image = request_files['file']
    image_obj = SmartCamera.objects.create(image=image)
    image_url = f"http://{request.get_host()}{image_obj.image.url}"
    smart_camera = SmartCameraService()
    generate_response = smart_camera.generate(image_url=image_url)
    content = generate_response['choices'][0]['message']['content']
    return JsonResponse({'content': content})


def chatgptplus(request) -> HttpResponse:
    return render(request, 'chatgptplus.html')


@csrf_exempt
def generate_chatgptplus(request) -> JsonResponse:
    request = request.POST
    content = request['content']
    chatgpt_plus = ChatGPTPlusService()
    response = chatgpt_plus.generate(content=content)
    return JsonResponse(response)
