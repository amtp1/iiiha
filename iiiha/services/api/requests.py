import time
import json
import base64
from dataclasses import dataclass

import requests
from django.conf import settings

from ..temp.temp import messages, food_messages


class AssistantRequestService:
    def __init__(self):
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'

    def generate(self, content: str):
        data = {'model': 'gpt-4o-mini', 'messages': messages(content),
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
        data = {'model': 'gpt-4o-mini', 'messages': [{'role': 'user', 'content': content}],
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

    def check_generation(self, uuid, attempts=10, delay=20):
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
    @dataclass
    class SmartCameraAsstId:
        main = 'asst_R8urIWSIEAfJLJd3Un1fZQ19'
        beer = 'asst_9wiloBO5MJmUETNl2uycKoH5'
        whiskey = 'asst_1JPJoSReXjL0u04T61azD7gU'
        wine = 'asst_dZJs90A8rlxbYbVRHlHPchaz'
        diplom = 'asst_LHTzmbG7vHf6SIKRerh8HTFj'
        movie = 'asst_AcXImnyaMZx13AFDC5TzcR2x'
        medicine = 'asst_2pmAWoQb6A7ZErDyJpnvxUNE'
        fat = 'asst_6zwpttlszuU01VPtFvQct5lf'
        food = 'asst_8DrxNX02LfyqekxqXibcBWrw'
        auto = 'asst_IDGYZ1cF5QsM2fddezaRT23U'
        cynologist = 'asst_JKJue14SrbWCdgX7eEO5Q17F'
        polyglot = 'asst_qrMbAqVawxnRWCKI9FybYX9g'
        guide = 'asst_KBuHlKwvsofuufHBEAjoQK9E'
        botanist = 'asst_yNOzqzIOWjDHsdxt7ebGELm0'
        zoologist = 'asst_8zGAhZh9GXX3CrEvRs8MgtF5'
        art = 'asst_mH4utaJ8pVOYalo5vbXrvrZH'

    def __init__(self):
        self.URL = 'https://api.openai.com/v1/chat/completions'
        self.AUTH_HEADERS = {
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        self.ASST_AUTH_HEADERS = {
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}',
            'Content-Type': 'application/json',
            'OpenAI-Beta': 'assistants=v2'
        }

        self.BASE_IMAGE = None

    def generate_main_asst(self):
        url = f'https://api.openai.com/v1/assistants/{self.SmartCameraAsstId().main}'
        request = requests.get(url=url, headers=self.ASST_AUTH_HEADERS)
        response = request.json()
        return response

    def generate_asst_by_id(self, asst_id):
        url = f'https://api.openai.com/v1/assistants/{asst_id}'
        request = requests.get(url=url, headers=self.ASST_AUTH_HEADERS)
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
        response = requests.post(url=self.URL, json=payload, headers=self.AUTH_HEADERS)
        data = response.json()
        content = data['choices'][0]['message']['content']
        return content

    def check_asst_content_response(self, content):
        if content == 'main':
            asst_name = 'Основной ассистент'
            return {'asst_name': asst_name, 'content': self.generate()}
        elif content == 'beer':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.beer)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'whiskey':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.whiskey)
            return self.generate(asst.get('instructions'))
        elif content == 'wine':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.wine)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'diplom':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.diplom)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'movie':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.movie)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'medicine':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.medicine)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'fat':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.fat)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'food':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.food)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'auto':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.auto)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'cynologist':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.cynologist)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'polyglot':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.polyglot)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'guide':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.guide)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'botanist':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.botanist)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'zoologist':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.zoologist)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}
        elif content == 'art':
            asst = self.generate_asst_by_id(self.SmartCameraAsstId.art)
            return {'asst_name': asst.get('name'), 'content': self.generate(asst.get('instructions'))}

    def encode_image(self, image_file):
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_image

    def main(self, image_file):
        self.BASE_IMAGE = self.encode_image(image_file)
        asst_instruction = self.generate_main_asst().get('instructions')
        check_response = self.check_asst_content_response(self.generate(asst_instruction))
        return check_response


class FoodAssistantRequestService:
    def __init__(self):
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'
        self.AUTH_HEADERS = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
        }

    def generate(self, content: str):
        data = {'model': 'gpt-4o-mini', 'messages': food_messages(content),
                'temperature': 0.7}

        request = requests.post(url=self.BASE_URL, json=data, headers=self.AUTH_HEADERS)
        response = json.loads(request.text)
        return response


class ChatGPTRequestService:
    def __init__(self):
        self.BASE_URL = 'https://api.openai.com/v1/chat/completions'
        self.AUTH_HEADERS = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {settings.GPT_SECRET_KEY}'
        }

    def generate(self, content: str, temperature: float):
        data = {'model': 'gpt-4o-mini',
                'messages': [{'role': 'system', 'role': 'assistant',
                              'role': 'user', 'content': content}],
                'temperature': temperature}

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
