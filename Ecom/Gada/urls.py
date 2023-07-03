from django.urls import path
from .views import *


urlpatterns = [

    path('signup', signup_form, name = 'signup'),
    path('login', loginpage, name = 'login'),
    path('',homepage, name = 'home'),
    path('logout',logout, name = 'logout'),
    path('cart/<int:pk>',cart, name = 'cart'),
    path('remove/<int:pk>',remove, name = 'remove'),
    path('cartview',cart_view, name = 'cartview'),
    path('ship',shipping, name = 'ship'),
    path('payment',payment, name = 'payment'),
    path('removeitem/<int:pk>',removeitem, name = 'removeitem'),
    path('details/<int:pk>',details, name = 'details'),
]