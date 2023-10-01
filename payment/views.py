import stripe
import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from orders.views import payment_confirmation

@login_required
def CartView(request):
    cart = Cart(request)
    total = str(cart.get_total_price())
    total = total.replace('.','')
    total = int(total)
    stripe.api_key = 'sk_test_51NEXcOJKvethcrHmWHGgiyvcWn3m6c6v8k9Ter0kgCes436AogZth2Ukq828YirZrs0JWdl6xKOcP2G3nfu7JQs3004EjABz9w'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )
    return render(request,'payment/home.html',{'client_secret':intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    print('trye tyr try try try try')

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        print('yes yes yes yes yes')
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def order_placed(request):
    cart = Cart(request)
    cart.clear()
    return render(request,'payment/orderplaced.html')
