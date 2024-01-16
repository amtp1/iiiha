import json

import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from services.api.requests import *


def index(request) -> HttpResponse:
    return render(request, "index.html")


def chatgpt(request) -> HttpResponse:
    return render(request, "chatgpt.html")


@csrf_exempt
def generate_assistent_request(request):
    content = request.POST['content']
    assistent_request = AssistentRequest()
    response = assistent_request.generate(content)
    return JsonResponse(response)


@csrf_exempt
def generate_chatgpt(request) -> JsonResponse:
    request = request.POST
    content = request['content']
    chat_gpt = ChatGPT()
    response = chat_gpt.generate(content=content)
    return JsonResponse(response)


def fusion(request) -> HttpResponse:
    return render(request, 'fusion.html')


@csrf_exempt
def generate_fusion(request) -> JsonResponse:
    request = request.POST
    prompt = request['prompt']
    fusion = Fusion()
    uuid = fusion.generate(prompt=prompt)
    response = fusion.check_generation(uuid=uuid)
    return JsonResponse({'image': response})


def plusvector(request) -> HttpResponse:
    return render(request, 'plusvector.html')


@csrf_exempt
def generate_plusvector(request) -> JsonResponse:
    request = request.POST
    prompt = request['prompt']
    plus_vector = PlusVector(prompt=prompt)
    plus_vector_response = plus_vector.get()
    return JsonResponse({'images': plus_vector_response['response']['concepts']['images']})
