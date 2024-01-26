from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, HttpRequest
from rest_framework.generics import ListAPIView
from rest_framework import authentication, permissions

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
    generate_data = smart_camera.generate(image_url=image_url)
    content = f"Опиши в деталях и цифрах этот объект как можно больше: {generate_data['name']}"
    chat_gpt = ChatGPTService()
    chat_gpt_response = chat_gpt.generate(content=content)
    description = chat_gpt_response['choices'][0]['message']['content']
    return JsonResponse({'name': generate_data['name'], 'description': description})
