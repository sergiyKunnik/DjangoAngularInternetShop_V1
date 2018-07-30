"""TestInternetShop_DjangoAget_categoriesngular URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path
from api.views import users_views, cart_views, views

urlpatterns = [
    re_path(r'^register/$', users_views.register),
    re_path(r'^login/$', users_views.login),
    re_path(r'^add_to_cart/$', cart_views.add_to_cart),
    re_path(r'^remove_from_cart/$', cart_views.remove_from_cart),
    re_path(r'^edit_cart/$', cart_views.edit_cart),
    re_path(r'^create_order/$', cart_views.create_order),
    re_path(r'^get_categories/$', views.get_categories),
    re_path(r'^get_products/$', views.get_products),
    re_path(r'^get_products_by_category/(?P<category_id>[0-9]+)/$', views.get_products_by_category),
    re_path(r'^product_detail/(?P<product_id>[0-9]+)/$', views.product_detail),
]
