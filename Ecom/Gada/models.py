from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True)
    username = models.CharField(max_length=20)
    avatar = models.ImageField(null=True, default='xyz.jpeg')
    password = models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS= []
    
    def __str__(self) -> str:
        return self.username
        

class Product(models.Model):

    name = models.CharField(max_length=200)
    price = models.IntegerField()
    category = models.CharField(max_length=200, null=True)
    description = models.TextField()
    digital = models.BooleanField(default=False)
    image = models.ImageField(null = True)

    def __str__(self):
        return self.name


class Cart(models.Model):
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     item = models.ForeignKey(Product , on_delete=models.CASCADE)
     quantity = models.IntegerField(default=0)
     created = models.DateTimeField(auto_now_add=True)

     def __str__(self) -> str:
         return f'{self.quantity} of {self.user.name}'
     
     


class Order(models.Model):
    orderitems = models.ManyToManyField(Cart)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created =models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, blank = True, on_delete=models.CASCADE)
    city = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)


    def __str__(self) -> str:
        return self.user.username