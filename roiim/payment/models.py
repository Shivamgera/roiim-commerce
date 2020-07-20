import requests
import json
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from ..product.models import Product, AuditModel


class CardDetails(AuditModel):
    card_number = models.CharField(max_length=16, unique=True)
    expiry_month = models.CharField(max_length=2)
    expiry_year = models.CharField(max_length=4)
    holder_name = models.CharField(max_length=128)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='card')

    @staticmethod
    def save_card(card_number, expiry_month, expiry_year, holder_name, user):
        if not CardDetails.objects.filter(card_number=card_number).exists():
            CardDetails.objects.create(card_number=card_number, expiry_month=expiry_month, expiry_year=expiry_year,
                holder_name=holder_name, user=user)

class Payment(AuditModel):
    STATUS_SUCCESS = 1
    STATUS_ERROR = 2
    STATUS_IN_PROCESS = 0
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='payment')
    card = models.ForeignKey(CardDetails, on_delete=models.CASCADE)
    status = models.IntegerField(blank=True)
    token = models.CharField(max_length=128, blank=True)

    @staticmethod
    def create_payment(product, cardnumber, status):
        card = CardDetails.objects.get(card_number=cardnumber)
        payment = Payment.objects.create(product=product, card=card, status=status)
        payment.save()
        return payment


    @staticmethod
    def create_payment_handle(card_number, expiry_month, expiry_year,
        holder_name, cv_code, amount, nickname,
        street, city, postal_code, country, product):
        payment = Payment.create_payment(product=product, cardnumber=card_number, status=Payment.STATUS_IN_PROCESS)
        url = "https://api.test.paysafe.com/paymenthub/v1/paymenthandles"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic {}'.format(settings.BASE64_API_KEY),
        'Simulator': '"EXTERNAL"'
        }
        payload = {
            'merchantRefNum': payment.id,
            'transactionType': "PAYMENT",
            'card': {
                'cardNum': card_number,
                'cardExpiry':{
                    'month': expiry_month,
                    'year': expiry_year
                    },
                'cvv': cv_code,
                "holderName": holder_name,
                },
            "paymentType": "CARD",
            "amount": int(amount),
            "currencyCode": "USD",
            "billingDetails": {
                "nickName": nickname,
                "street": street,
                "city": city,
                "zip": postal_code,
                "country": country
            },
            "returnLinks": [{
            "rel": "on_completed",
            "href": "http://shivam-app.com/payment/{}/details/success".format(product.id),
            # 'href': reverse('payment:success' kwargs={'payment_pk':payment.id, 'paymentHandleToken'}),
            "method": "GET"
            },
            {
            "rel": "on_failed",
            "href": "http://shivam-app.com/products/",
            "method": "GET"
            },
            {
            "rel": "default",
            "href": "http://shivam-app.com/products/",
            "method": "GET"
            }
            ]            
        }
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data = payload)
        r = response.json()
        if response.status_code == 201:
            payment.token = r['paymentHandleToken']
            payment.save(update_fields=['token'])
        print(response.status_code)
        
        print(response.text.encode('utf8'))
        return response
    
    @staticmethod
    def pay_for_product(product, payment):
        url = "https://api.test.paysafe.com/paymenthub/v1/payments"
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic {}'.format(settings.BASE64_API_KEY),
        'Simulator': '"EXTERNAL"'
        }
        payload = {
        "merchantRefNum": payment.id,
        "amount": int(product.price),
        "currencyCode": "USD",
        "dupCheck": "true",
        "settleWithAuth": "false",
        "paymentHandleToken": payment.token,
        "description": product.description
        } 
        payload = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data = payload)
        r = response.json()
        if response.status_code == 201 and r['status'] == 'COMPLETED':
            payment.status = Payment.STATUS_SUCCESS
            payment.save(update_fields=['status'])
        else:
            payment.status = Payment.STATUS_ERROR
            payment.save(update_fields=['status'])
        print(response.text)
        return response