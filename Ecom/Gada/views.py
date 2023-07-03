from django.shortcuts import render, redirect
from .forms import UserForm,LoginForm
from .models import *
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from django.conf import settings
import stripe

# Create your views here.
def signup_form(request):
    if request.user.is_authenticated:
        return redirect('home')
    page = 'signup'
    form = UserForm()
    context = {'form': form}

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid:
            obj =  form.save(commit=False)
            obj.avatar = request.FILES.get('image')
            obj.save()
            return redirect('signup')
        

    return render(request, 'form.html',{'form':form,'page':page,'title':'signup'})


def loginpage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email = email)

        except:
            return HttpResponse('User does not exist')

        user = authenticate(email = email, password = password)

        if user:
            login(request, user)
            return redirect('home')


    return render(request, 'form.html',{'title':'login'})

def logoutpage(request):
 
    logout(request)

    

def homepage(request):
    query = request.GET.get('q') if request.GET.get('q')!= None else ''
    product = Product.objects.filter(Q(name__icontains =query) | Q(category__icontains =query)).order_by('-price') 
    
    alls = Product.objects.all()
    
    context = {'product':product,'user':request.user,'alls':alls, 'title':'home'}
    

    return render(request,'home.html',context)


@login_required(login_url='login')
def cart(request,pk):
    
    if request.user.is_authenticated:
        item = Product.objects.get(id =pk)
        

        order_item, created = Cart.objects.get_or_create(user = request.user , item = item ,)
         
        order_qs =Order.objects.filter(user = request.user , ordered = False)

        if order_qs.exists():
            order = order_qs[0] 

            if order.orderitems.filter(item = item).exists:
                order_item.quantity +=1
                order_item.save()
                messages.info(request,'added successfully,.,,' )
                return redirect('cartview')
            
            else:
                order.orderitems.add(order_item)
                messages.info(request,'added successfullyfad')
                return redirect('cartview')
        else:
            order = Order.objects.create(user = request.user)
            order.orderitems.add(order_item)
            messages.info(request,'added successfullydada')
            return redirect('cartview')

        

def remove(request,pk):
    
    if request.user.is_authenticated:
        item = Product.objects.get(id = pk)

        cart_qs = Cart.objects.filter(user = request.user, item = item)

        if cart_qs.exists():
                cart = cart_qs[0]
                if cart.quantity <=0:
                    cart.delete()

                else:
                    cart.quantity -=1
                    cart.save()

        
        order_qs = Order.objects.filter(user = request.user, ordered = False)

        if order_qs.exists():
            order = order_qs[0]

            if order.orderitems.filter(item = item).exists():
                order_item = Cart.objects.filter(item = item , user = request.user)[0]
                order.orderitems.remove(order_item)

                return redirect('cartview')
            
            else:
                return redirect('cartview')


    else:
        return redirect('cartview')


def cart_view(request):
    cart = Cart.objects.filter(user =request.user)

    p =0
    for i in cart:
       
      p += i.item.price * i.quantity


    
    order_cart = Order.objects.filter(user = request.user , ordered =False)
    total = order_cart[0].orderitems.count
    context ={
        'total':total,
        'cart':cart,
        'p':p,
        'title' : 'cart'
    }


    return render(request,'cart.html',context)


@login_required(login_url='login')
def shipping(request):

    page = 'shipping'
    form = ShippingForm()
    cart = Cart.objects.filter(user =request.user)
    p =0
    
    for i in cart:
       p += i.item.price * i.quantity

    order_cart = Order.objects.get(user = request.user , ordered =False)
    
    total = order_cart.orderitems.count
    context ={'page':page,
              'form':form,
              'total':total,
              'cart':cart,
              'p':p,
              'title': 'shipping'
             }
    
    if request.method == 'POST':
        order_cart.ordered == True
        form = ShippingForm(request.POST)
        if form.is_valid():
            
            obj =form.save(commit=False)
            obj.user = request.user
            obj.order = order_cart
            obj.save()
            

            
            
            return HttpResponse('You will receive soon')

    

    return render(request, 'cart.html',context)


def payment(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    order_qs = Order.objects.filter(user = request.user, ordered = False)
    cart = Cart.objects.filter(user =request.user)
    p =0
    
    for i in cart:
       p += i.item.price * i.quantity

    if request.method == 'POST':
        charge = stripe.Charge.create(amount = p)
        currency = 'usd',
        description = order_qs
        source = request.POST['stripeToken']


    
    return render(request, 'payment.html', {'key':key,'total':p})

def removeitem(request, pk):

    item = Cart.objects.get(id =pk)
    item.delete()
    return redirect('cartview')


def details(request, pk):
    item = Product.objects.get(id = pk)

    return render(request,'details.html',{'item':item})