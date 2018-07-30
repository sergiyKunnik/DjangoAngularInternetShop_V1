import json

from django.contrib.auth.models import User
from api.models import Cart
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)

        if body['password'] != body['password1']:
            return JsonResponse({'status': False, 'message': 'error passwords'})

        try:
            User.objects.get(username=body['username'])
            return JsonResponse({'status': False})
        except User.DoesNotExist:
            user = User(username=body['username'], password=body['password'], email=body['email'])
            user.save()
            cart = Cart(user=user)
            cart.save()
            return JsonResponse({'status': True})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        try:
            user = User.objects.get(username=body['username'], password=body['password'])
            cart = Cart.objects.get(user=user)
            cart_items = []
            for item in cart.cart_items.all():
                cart_items.append({
                    'qty': item.qty,
                    'cart_item_total_price': item.cart_item_total_price,
                    'item_id': item.id,
                    'product': {
                        'product_id': item.product.id,
                        'title': item.product.title,
                        'price': item.product.price,
                    }
                })

            return JsonResponse({
                'status': True,
                'user': {
                    'username': user.username,
                    'password': user.password,
                    'email': user.email,
                },
                'cart': {
                    'cart_total_price': cart.cart_total_price,
                    'cart_items': cart_items,
                    'cart_id': cart.id,
                }
            })
        except User.DoesNotExist:
            return JsonResponse({'status': False})
