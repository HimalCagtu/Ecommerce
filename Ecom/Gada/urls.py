from django.urls import path
from .views import *

from django.contrib.auth.views import (
    
    
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetDoneView,

    )

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
    path('profile',profile, name = 'profile'),
    path('changepassword',changepassword, name = 'changepassword'),
    path('password-reset/', PasswordResetView.as_view(template_name='passowordrest.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='reset_password_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('passwordresetcomplete/',passwordresetcomplete,name='password_reset_complete'),
]




