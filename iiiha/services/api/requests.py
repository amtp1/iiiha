import time
import json

import requests
from django.conf import settings

from ..temp.temp import messages, food_messages


class AssistentRequestService:
    def __init__(self):
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'

    def generate(self, content: str):
        data = {'model': 'gpt-3.5-turbo', 'messages': messages(content),
                'temperature': 0.7
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
        }
        request = requests.post(url=self.BASE_URL, json=data, headers=headers)
        response = json.loads(request.text)
        return response


class ChatGPTService:
    def __init__(self):
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'

    def generate(self, content=None):
        data = {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': content}],
                'temperature': 0.7
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
        }
        request = requests.post(url=self.BASE_URL, json=data, headers=headers)
        response = json.loads(request.text)
        return response


class FusionService:
    def __init__(self):
        self.URL = 'https://api-key.fusionbrain.ai/'
        self.AUTH_HEADERS = {
            'X-Key': f'Key {settings.FUSION_API_KEY}',
            'X-Secret': f'Secret {settings.FUSION_SECRET_KEY}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, self.get_model()),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, uuid, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + uuid, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


class PlusVectorService:
    def __init__(self, prompt: str):
        self.URL = 'https://api.plusvector.com/'
        self.AUTH_HEADERS = {
            'Authorization': f'Bearer {settings.PLUSVECTOR_API_KEY}'
        }
        self.prompt = prompt

    def create(self):
        data = {
            'prompt': self.prompt,
            'webhook': None
        }

        response = requests.post(self.URL + 'render/create', data=data, headers=self.AUTH_HEADERS)
        data = response.json()
        return data

    def get(self, attempts=10, delay=10):
        create_response = self.create()
        generate_id = create_response['response']['id']

        payload = {
            'id': generate_id
        }

        while attempts > 0:
            response = requests.get(self.URL + 'render', params=payload, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['success'] == True:
                if 'concepts' in data['response'].keys():
                    if data['response']['concepts']:
                        return data
            attempts -= 1
            time.sleep(delay)


class SmartCameraService:
    def __init__(self):
        self.URL = 'https://api.task-tiker.ru/api.php'
        self.AUTH_HEADERS = {
            'Authorization': f'Bearer {settings.SMARTCAMERA_API_KEY}',
            'Content-Type': 'application/json'
        }

    def generate(self, image_url):
        payload = {'action': 'yandex_picture', 'url_picture': image_url}
        response = requests.post(url=self.URL, json=payload, headers=self.AUTH_HEADERS)
        data = response.json()
        return data


class FoodAssistentRequestService:
    def __init__(self):
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'
        self.AUTH_HEADERS = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
        }

    def generate(self, content: str):
        data = {'model': 'gpt-3.5-turbo', 'messages': food_messages(content),
                'temperature': 0.7}

        request = requests.post(url=self.BASE_URL, json=data, headers=self.AUTH_HEADERS)
        response = json.loads(request.text)
        return response


class ChatGPTPlusService:
    def __init__(self):
        self.BASE_URL = 'https://api.theb.ai/v1/chat/completions'
        self.AUTH_HEADERS = {
            'Authorization': f'Bearer {settings.CHATGPT_PLUS}',
            'Content-Type': 'application/json'
        }

    def generate(self, content: str):
        payload = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'user',
                    'content': content
                }
            ],
            'stream': False,
            'model_params': {
                'temperature': 1
            }
        }
        request = requests.post(url=self.BASE_URL, json=payload, headers=self.AUTH_HEADERS)
        response = request.json()
        return response
