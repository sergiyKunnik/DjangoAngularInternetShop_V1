import json

from django.contrib.auth.models import User

from api.models import Product, CartItem, Order, Cart
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail


@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            product = Product.objects.get(id=body['product_id'])
            if product.add_to_cart(body['cart_id'], body['qty']):
                return JsonResponse({'status': True})
            else:
                return JsonResponse({'status': False})
        except:
            return JsonResponse({'status': False})


@csrf_exempt
def remove_from_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            cart_item = CartItem.objects.get(id=body['cart_item_id'])
            cart_item.remove_from_cart(body['cart_id'])
            cart_item.delete()
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})


@csrf_exempt
def edit_cart(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        try:
            cart_item = CartItem.objects.get(id=int(body['cart_item_id']))
            cart_item.edit_cart(int(body['cart_item_qty']))
            return JsonResponse({'status': True})
        except:
            return JsonResponse({'status': False})


@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        cart = Cart.objects.get(id=int(body['cart_id']))
        order = Order(username=cart.user.username,
                      email=cart.user.email,
                      total_price=cart.cart_total_price,
                      desc=body['desc'],
                      )
        order.save()
        order.cart_items.add(*cart.cart_items.all())
        cart.cart_items.clear()
        cart.update_price()
        email_list = []
        for user in User.objects.filter(is_superuser=True):
            email_list.append(user.email)
        send_mail(
            'New order',
            'username =>' + order.username,
            'from@example.com',
            [email_list],
        )
        print(email_list)
        return JsonResponse({
            'status': True,
            'email': cart.user.email,
            'username': cart.user.username,
        })
