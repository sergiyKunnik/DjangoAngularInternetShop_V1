from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Назва категорії')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категорії'
        verbose_name = 'Категорія'


class Product(models.Model):
    title = models.CharField(max_length=200, default=None, verbose_name='Назва Товару')
    price = models.PositiveIntegerField(default=0, verbose_name='Ціна')
    text = models.TextField(default=None, verbose_name='Опис товару')
    category = models.ForeignKey(Category, on_delete=None, verbose_name='Категорія')
    image = models.ImageField(upload_to='product/images', default=None, verbose_name='Зображення продукту')

    def add_to_cart(self, cart_id, qty):
        cart = Cart.objects.get(id=cart_id)

        for item in cart.cart_items.all():
            if item.product.id == int(self.id):

                return False
        cart_item = CartItem(product=self)
        cart_item.qty = int(qty)
        cart_item.update_price()
        cart_item.save()
        cart_item.update_price()

        cart.cart_items.add(cart_item)
        cart.save()
        cart.update_price()
        return True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Товари'
        verbose_name = 'Товар'


class CartItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=None,
                                verbose_name='Товар',
                                default=None,
                                related_name='cart_item_product')
    qty = models.PositiveIntegerField(default=1, verbose_name='Кількість')
    cart_item_total_price = models.PositiveIntegerField(verbose_name='Загальна вартість', default=0)

    def remove_from_cart(self, cart_id):
        cart = Cart.objects.get(id=int(cart_id))
        cart.cart_items.remove(self)
        cart.update_price()

    def update_price(self):
        self.cart_item_total_price = self.qty * self.product.price

        self.save()

    def edit_cart(self, qty):
        self.qty = qty
        self.update_price()
        cart = Cart.objects.filter(cart_items__id=self.id)[0]
        cart.update_price()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Елементи корзини'
        verbose_name = 'Елемент корзини'


class Cart(models.Model):
    cart_items = models.ManyToManyField(CartItem, default=None, blank=True, verbose_name='Елементи корзини')
    cart_total_price = models.PositiveIntegerField(default=0,
                                                   verbose_name='Загільна вартість всієї покупки',
                                                   blank=True)
    user = models.ForeignKey(User, on_delete=None, default=None, verbose_name='Користувач')

    def update_price(self):
        self.cart_total_price = 0
        for item in self.cart_items.all():
            self.cart_total_price += item.cart_item_total_price
        self.save()

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name_plural = 'Корзини'
        verbose_name = 'Корзина'


class Order(models.Model):
    username = models.CharField(max_length=200, verbose_name='Контактна особа', default=None)
    email = models.CharField(max_length=200, verbose_name='email', default=None)
    cart_items = models.ManyToManyField(CartItem, default=None, blank=True, verbose_name='Товари')
    total_price = models.PositiveIntegerField(default=0, verbose_name='Загільна вартість покупки')
    desc = models.TextField(default=None, verbose_name='Додаткова інформація', blank=True)

    def __str__(self):
        return self.username + '=>' + self.email

    class Meta:
        verbose_name_plural = 'Замовлення'
        verbose_name = 'Замовлення'
