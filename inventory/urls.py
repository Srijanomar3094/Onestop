from django.urls import path
from inventory import views

urlpatterns = [
    path('register/', views.register),
    path('login_view/', views.login_view, name='login_view'),
    path('inventory/', views.inventory, name='inventory'),
    path('product/', views.product, name='product'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('buy/', views.buy, name='buy'),
   # path('inventory_image_upload/', views.inventory_image_upload, name='inventory_image_upload'),




]

