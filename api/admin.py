from django.contrib import admin
from .models import CartItem, Cart, Category, Product, Order
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
admin.site.register(Product)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'total_price']
