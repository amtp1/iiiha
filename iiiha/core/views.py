import json

import requests
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def index(request) -> HttpResponse:
    return render(request, "index.html")


def chatgpt(request) -> HttpResponse:
    return render(request, "chatgpt.html")

@csrf_exempt
def generate_chatgpt(request) -> JsonResponse:
    request = request.POST
    content = request['content']
    url = 'https://api.openai.com/v1/chat/completions'
    data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': content}],
            'temperature': 0.7
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
    }
    generate_request = requests.post(url=url, json=data, headers=headers)
    response = json.loads(generate_request.text)
    return JsonResponse(response)
