from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model

# Register your models here.
user = get_user_model()
admin.site.register(user)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Shipping)

admin.site.register(Order)

