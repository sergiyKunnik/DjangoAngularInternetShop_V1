from django.contrib.auth.models import User
from api.models import Cart, Product, CartItem, Category
from django.http import JsonResponse
# Create your views here.
from django.views.decorators.csrf import csrf_exempt


def get_categories(request):
    if request.method == 'GET':
        return JsonResponse({
            'status': True,
            'categories': list(Category.objects.all().values('name', 'id'))
        })


def get_products(requets):
    if requets.method == 'GET':
        return JsonResponse({
            'status': True,
            'products': list(Product.objects.all().values('title', 'price', 'id', 'image', 'text'))
        })


def get_products_by_category(request, category_id):
    if request.method == 'GET':
        category = Category.objects.get(id=category_id)
        return JsonResponse({
            'status': True,
            'products': list(Product.objects.filter(category=category).values('title', 'price', 'id', 'image', 'text'))
        })


def product_detail(request, product_id):
    if request.method == 'GET':
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'status': True,
            'products': {
                'title': product.title,
                'price': product.price,
                'text': product.text,
                'image': product.image.url,
                'id': product.id,
            }
        })