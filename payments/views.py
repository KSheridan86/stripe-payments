from django.shortcuts import render
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
import stripe


class HomePageView(TemplateView):
    template_name = 'home.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'https://8000-ksheridan86-stripepayme-mubu0huq1w6.ws-eu79.gitpod.io/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                            'description': 'Comfortable cotton t-shirt',
                            'price_data': {
                                'currency': 'usd',
                                'unit_amount': 2000,
                                'product_data': {
                                    'name': 'T-shirt',
                                    'description': 'Comfortable cotton t-shirt',
                                    'images': ['https://example.com/t-shirt.png'],
                                    },
                                },
                            'quantity': 1,
                            }],
                mode='payment',
                success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url='https://example.com/cancel',
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
