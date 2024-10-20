import json

from django.conf import settings
from django.http import JsonResponse
from rest_framework import generics
from yookassa import Configuration, Payment


from core.models import Payment as Payment_Model
from core.serializers import PaymentSerializer
from iiiha.settings import YOOKASSA_SECRET_KEY, YOOKASSA_SHOP_ID


Configuration.account_id = YOOKASSA_SHOP_ID
Configuration.secret_key = YOOKASSA_SECRET_KEY


class PaymentAPI:
    def get_payment_url(self, price, tariff_id, format=None):
        # data = json.loads(request.POST['data'])
        payment = Payment.create({
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "payment_method_data": {
                "type": "bank_card"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": 'https://ixa.su'  # settings.REDIRECT_URL
            },
            "capture": True,
            "description": tariff_id
        })
        payment_data = json.loads(payment.json())
        payment_id = payment_data['id']
        payment_url = (payment_data['confirmation'])['confirmation_url']
        description = payment_data['description']
        return {"status_code": 200, "payment_id": payment_id, "payment_url": payment_url, 'description': description}

    def check_payment(self, payment_id, format=None):
        payment = json.loads(Payment.find_one(payment_id).json())
        if payment['status'] == 'succeeded':
            return {"status_code": 200, "message": True}
        return {"status_code": 400, "message": False}
