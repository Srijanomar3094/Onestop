from django.urls import path
from inventory import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('register/', views.register),
    path('login_view/', views.login_view, name='login_view'),
    path('inventory/', views.inventory, name='inventory'),
    path('product/', views.product, name='product'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('buy/', views.buy, name='buy'),
    path('logout_view/', views.logout_view, name='logout_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





