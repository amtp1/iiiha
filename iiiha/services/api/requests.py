import time
import json
import base64
import logging
from logging.config import fileConfig

import requests
from django.conf import settings
from requests.exceptions import JSONDecodeError

from ..temp.temp import food_messages
from core.models import *
from loguru import logger


log_path = 'core/log/services'


class Config:
    def __init__(self):
        self.GPT_AUTH_HEADERS = {
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}',
            'Content-Type': 'application/json'
        }

        self.ASST_AUTH_HEADERS = {
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}',
            'Content-Type': 'application/json',
            'OpenAI-Beta': 'assistants=v2'
        }


class AssistantRequestService(Config):
    def __init__(self):
        super().__init__()
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'
        logger.add(f"{log_path}/gpt/assistant/debug.log")

    def generate_main_asst(self):
        url = 'https://api.openai.com/v1/assistants/asst_h1t8ISoM3fX0ZwZR1DS83Unj'
        request = requests.get(url=url, headers=self.ASST_AUTH_HEADERS)
        response = request.json()
        return response

    def generate(self, content: str):
        asst_response = self.generate_main_asst()
        data = {'model': 'gpt-4o-mini', 'messages': [
                        {"role": "user", "content": [
                            {"type": "text", "text": asst_response.get('instructions')},
                            {"type": "text", "text": content}
                            ]},
                    ]
                }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
        }
        request = requests.post(url=self.BASE_URL, json=data, headers=headers)
        response = json.loads(request.text)
        if request.status_code != 200:
            logger.error(response)
        return response


class ChatGPTService:
    def __init__(self):
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'
        logger.add(f"{log_path}/gpt/chat/debug.log")

    def generate(self, content=None):
        data = {'model': 'gpt-4o-mini', 'messages': [{'role': 'user', 'content': content}],
                'temperature': 0.7
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
        }
        request = requests.post(url=self.BASE_URL, json=data, headers=headers)
        response = json.loads(request.text)
        logger.info(response)
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
        logger.info(data)
        return data['uuid']

    def check_generation(self, uuid, attempts=10, delay=20):
        while True:
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


class SmartCameraService(Config):
    def __init__(self):
        super().__init__()
        self.URL = 'https://api.openai.com/v1/chat/completions'

        self.BASE_IMAGE = None

    def generate_main_asst(self):
        main_asst = Assistants.objects.get(key_word='main')
        url = f'https://api.openai.com/v1/assistants/{main_asst.asst_id}'
        request = requests.get(url=url, headers=self.ASST_AUTH_HEADERS)
        response = request.json()
        return response

    def generate_asst_by_id(self, asst_id):
        url = f'https://api.openai.com/v1/assistants/{asst_id}'
        request = requests.get(url=url, headers=self.ASST_AUTH_HEADERS)
        response = request.json()
        return response

    def yandex(self):
        url = 'https://api.webastera.ru/api.php'
        data = {'action': 'yandex_picture', 'url_picture': f"data:image/jpeg;base64,{self.BASE_IMAGE}"}
        request = requests.post(url=url, json=data)
        response = request.json()
        return response

    def generate(self, instruction=""):
        payload = {'model': 'gpt-4o-mini',
                   'messages': [
                        {"role": "user", "content": [
                            {"type": "text", "text": instruction if instruction != "" else "Что на картинке?"},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{self.BASE_IMAGE}"}}
                            ]}
                    ]}
        response = requests.post(url=self.URL, json=payload, headers=self.GPT_AUTH_HEADERS)
        data = response.json()
        content = data['choices'][0]['message']['content']
        return content

    def check_asst_content_response(self, content):
        content_data = {'asst_name': None, 'content': None, 'yandex_data': None}
        if content == 'main':
            content_data['asst_name'] = 'Основной ассистент'
            content_data['content'] = self.generate()
        else:
            asst_obj = Assistants.objects.get(key_word=content)
            asst = self.generate_asst_by_id(asst_obj.asst_id)
            content_data['asst_name'] = asst.get('name')
            content_data['content'] = self.generate(asst.get('instructions'))

        try:
            yandex_gen_resp = self.yandex()
            content_data['yandex_data'] = {'name': yandex_gen_resp['name'], 'minPrice': yandex_gen_resp['minPrice'],
                                           'maxPrice': yandex_gen_resp['maxPrice']
                                           }
        except JSONDecodeError:
            return content_data
        return content_data

    def encode_image(self, image_file):
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_image

    def main(self, image_file):
        self.BASE_IMAGE = self.encode_image(image_file)
        asst_instruction = self.generate_main_asst().get('instructions')
        check_response = self.check_asst_content_response(self.generate(asst_instruction))
        return check_response


class FoodAssistantRequestService(Config):
    def __init__(self):
        super().__init__()
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'

    def generate(self, content: str):
        data = {'model': 'gpt-4o-mini', 'messages': food_messages(content),
                'temperature': 0.7}

        request = requests.post(url=self.BASE_URL, json=data, headers=self.GPT_AUTH_HEADERS)
        response = json.loads(request.text)
        return response


class ChatGPTRequestService(Config):
    def __init__(self):
        super().__init__()
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'

    def generate(self, content: str, temperature: float):
        data = {'model': 'gpt-4o-mini',
                'messages': [{'role': 'system', 'role': 'assistant',
                              'role': 'user', 'content': content}],
                'temperature': temperature}

        request = requests.post(url=self.BASE_URL, json=data, headers=self.GPT_AUTH_HEADERS)
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
            'model': 'gpt-4o-mini',
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
